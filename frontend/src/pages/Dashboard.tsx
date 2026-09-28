import type React from "react";
import { useEffect, useState } from "react";
import { FreshnessBadge } from "../components/FreshnessBadge";
import { ProvenanceBadge } from "../components/ProvenanceBadge";
import { RiskCard } from "../components/RiskCard";
import { farmService } from "../services/api";
import type { Farm, FarmContextResponse, FreshnessState } from "../types";

export const Dashboard: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [selectedFarmId, setSelectedFarmId] = useState<number | null>(null);
  const [context, setContext] = useState<FarmContextResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFarms();
  }, []);

  const loadFarms = async () => {
    try {
      const list = await farmService.listFarms();
      setFarms(list);
      if (list.length > 0) {
        setSelectedFarmId(list[0].id);
      }
    } catch (err: unknown) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (selectedFarmId) {
      loadContext(selectedFarmId);
    }
  }, [selectedFarmId]);

  const loadContext = async (farmId: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const ctx = await farmService.getFarmContext(farmId);
      setContext(ctx);
    } catch (err: unknown) {
      const msg =
        err instanceof Error
          ? err.message
          : "Failed to fetch farm context data.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  if (farms.length === 0) {
    return (
      <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm text-center space-y-4">
        <h1 className="text-2xl font-bold text-gray-900">
          AgriGuard AI — Welcome
        </h1>
        <p className="text-sm text-gray-600 max-w-lg mx-auto">
          To get started, please setup your first farm plot to enable
          context-aware weather, climate, soil, and crop disease intelligence.
        </p>
        <a
          href="/farm"
          className="inline-block px-5 py-2.5 bg-emerald-700 text-white rounded-lg text-sm font-semibold hover:bg-emerald-800"
        >
          Setup First Farm Plot &rarr;
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Header & Farm Selector */}
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Farm Intelligence Dashboard
          </h1>
          <p className="text-xs text-gray-600 mt-0.5">
            Real-time environmental context, short-term forecast, historical
            climate baseline, and risk signals.
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <label className="text-xs font-semibold uppercase text-gray-500 whitespace-nowrap">
            Select Farm:
          </label>
          <select
            value={selectedFarmId || ""}
            onChange={(e) => setSelectedFarmId(Number(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm font-semibold text-gray-800 focus:ring-2 focus:ring-emerald-500 focus:outline-none w-full md:w-64"
          >
            {farms.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name} ({f.primary_crop})
              </option>
            ))}
          </select>
        </div>
      </div>

      {isLoading && (
        <div className="p-8 text-center bg-white rounded-xl border border-gray-200 shadow-sm text-gray-500 text-sm">
          Loading farm context from Open-Meteo, NASA POWER, and Nominatim...
        </div>
      )}

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs font-semibold">
          {error}
        </div>
      )}

      {context && !isLoading && (
        <>
          {/* Location & Freshness Header */}
          <div className="bg-emerald-900 text-white p-5 rounded-xl shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-bold">
                  {context.location.display_name}
                </h2>
                <FreshnessBadge
                  state={
                    (context.freshness.weather as FreshnessState) ||
                    "unavailable"
                  }
                />
              </div>
              <div className="text-xs text-emerald-200 mt-1 flex gap-4 font-mono">
                <span>Lat: {context.location.latitude.toFixed(4)}°</span>
                <span>Lon: {context.location.longitude.toFixed(4)}°</span>
                {context.elevation && (
                  <span>Elevation: {context.elevation.elevation_m}m</span>
                )}
                <span>Crop: {context.farm.primary_crop}</span>
              </div>
            </div>

            {context.weather && (
              <ProvenanceBadge
                provider={context.weather.provenance.provider_name}
                quality={context.weather.provenance.data_quality}
              />
            )}
          </div>

          {/* Live Environmental Metrics Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="text-[11px] font-semibold text-gray-500 uppercase">
                Temperature
              </div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {context.weather?.temperature_c != null
                  ? `${context.weather.temperature_c}°C`
                  : "UNAVAILABLE"}
              </div>
              <div className="text-[10px] text-gray-400 mt-1">Ambient 2m</div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="text-[11px] font-semibold text-gray-500 uppercase">
                Humidity
              </div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {context.weather?.humidity_pct != null
                  ? `${context.weather.humidity_pct}%`
                  : "UNAVAILABLE"}
              </div>
              <div className="text-[10px] text-gray-400 mt-1">
                Relative Humidity
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="text-[11px] font-semibold text-gray-500 uppercase">
                Precipitation
              </div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {context.weather?.rainfall_mm != null
                  ? `${context.weather.rainfall_mm} mm`
                  : "UNAVAILABLE"}
              </div>
              <div className="text-[10px] text-gray-400 mt-1">Current Rain</div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="text-[11px] font-semibold text-gray-500 uppercase">
                Soil Moisture
              </div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {context.weather?.soil_moisture_m3m3 != null
                  ? `${context.weather.soil_moisture_m3m3} m³/m³`
                  : "UNAVAILABLE"}
              </div>
              <div className="text-[10px] text-gray-400 mt-1">Upper 0-1cm</div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="text-[11px] font-semibold text-gray-500 uppercase">
                Evapotranspiration
              </div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {context.weather?.et0_mm != null
                  ? `${context.weather.et0_mm} mm`
                  : "UNAVAILABLE"}
              </div>
              <div className="text-[10px] text-gray-400 mt-1">
                Reference ET0
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
              <div className="text-[11px] font-semibold text-gray-500 uppercase">
                VPD
              </div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {context.weather?.vpd_kpa != null
                  ? `${context.weather.vpd_kpa} kPa`
                  : "UNAVAILABLE"}
              </div>
              <div className="text-[10px] text-gray-400 mt-1">
                Vapour Pressure Deficit
              </div>
            </div>
          </div>

          {/* Risk Card */}
          <RiskCard riskContext={context.risk_context} />

          {/* 7-Day Forecast & Historical Climate */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
              <div className="flex justify-between items-center border-b pb-3">
                <h3 className="font-bold text-gray-900 text-sm">
                  7-Day Agroclimate Forecast
                </h3>
                <FreshnessBadge
                  state={
                    (context.freshness.weather as FreshnessState) ||
                    "unavailable"
                  }
                />
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
                {context.weather?.forecast ? (
                  context.weather.forecast.map((f, i) => (
                    <div
                      key={i}
                      className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-center space-y-1"
                    >
                      <div className="text-[11px] font-bold text-slate-700">
                        {f.date.slice(5)}
                      </div>
                      <div className="text-xs font-semibold text-slate-900">
                        {f.max_temp_c}° / {f.min_temp_c}°
                      </div>
                      <div className="text-[10px] text-blue-700 bg-blue-50 px-1 py-0.5 rounded">
                        ☔ {f.precipitation_mm ?? 0}mm
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="col-span-full text-xs text-gray-400 py-4 text-center">
                    Forecast data unavailable
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
              <div className="flex justify-between items-center border-b pb-3">
                <h3 className="font-bold text-gray-900 text-sm">
                  Historical Climate Baseline
                </h3>
                <FreshnessBadge
                  state={
                    (context.freshness.climate as FreshnessState) ||
                    "unavailable"
                  }
                />
              </div>
              {context.climate ? (
                <div className="text-xs space-y-2 text-gray-700">
                  <div className="flex justify-between">
                    <span>30-Day Total Rain:</span>
                    <span className="font-bold">
                      {context.climate.total_precipitation_mm ?? "--"} mm
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>7-Day Rain Sum:</span>
                    <span className="font-bold">
                      {context.climate.rainfall_7d_mm ?? "--"} mm
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Dry Spell Days:</span>
                    <span className="font-bold">
                      {context.climate.dry_spell_days ?? "--"} days
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Cumulative GDD:</span>
                    <span className="font-bold">
                      {context.climate.gdd_cumulative ?? "--"} °C-days
                    </span>
                  </div>
                  <div className="pt-2 border-t text-[11px] text-gray-500">
                    Source: {context.climate.provenance.provider_name}
                  </div>
                </div>
              ) : (
                <div className="text-xs text-gray-400 py-4 text-center">
                  Climate baseline data unavailable
                </div>
              )}
            </div>
          </div>

          {/* Provider Status & Health */}
          <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
            <h3 className="font-bold text-gray-900 text-sm border-b pb-3">
              External Data Provider Status & Health
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {context.provider_status.map((p) => (
                <div
                  key={p.provider_id}
                  className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs space-y-1"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-800">{p.name}</span>
                    <span
                      className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                        p.status === "healthy"
                          ? "bg-emerald-100 text-emerald-800"
                          : "bg-rose-100 text-rose-800"
                      }`}
                    >
                      {p.status.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-[10px] text-slate-500 flex justify-between">
                    <span>Category: {p.category}</span>
                    {p.latency_ms && <span>{p.latency_ms} ms</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
