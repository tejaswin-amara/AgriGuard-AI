import { useEffect, useState } from "react";
import {
  biodiversityService,
  environmentService,
  farmService,
  newsService,
  weatherService,
} from "../services/api";
import type {
  AirQualityData,
  BiodiversityData,
  ClimateData,
  ElevationData,
  Farm,
  NewsData,
  WeatherData,
} from "../types";

export const Insights: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [selectedFarm, setSelectedFarm] = useState<Farm | null>(null);
  const [activeTab, setActiveTab] = useState<
    "weather" | "climate" | "environment" | "biodiversity" | "news"
  >("weather");

  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [climate, setClimate] = useState<ClimateData | null>(null);
  const [airQuality, setAirQuality] = useState<AirQualityData | null>(null);
  const [elevation, setElevation] = useState<ElevationData | null>(null);
  const [biodiversity, setBiodiversity] = useState<BiodiversityData | null>(
    null,
  );
  const [news, setNews] = useState<NewsData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    farmService.listFarms().then((list) => {
      setFarms(list);
      if (list.length > 0) setSelectedFarm(list[0]);
    });
  }, []);

  useEffect(() => {
    if (!selectedFarm) return;
    setIsLoading(true);

    const lat = selectedFarm.latitude;
    const lon = selectedFarm.longitude;

    Promise.all([
      weatherService.getWeather(lat, lon).catch(() => null),
      weatherService.getClimate(lat, lon).catch(() => null),
      environmentService.getAirQuality(lat, lon).catch(() => null),
      environmentService.getElevation(lat, lon).catch(() => null),
      biodiversityService.getBiodiversity(lat, lon).catch(() => null),
      newsService
        .getAgriculturalNews(selectedFarm.primary_crop)
        .catch(() => null),
    ]).then(([w, c, aq, el, bio, nw]) => {
      setWeather(w);
      setClimate(c);
      setAirQuality(aq);
      setElevation(el);
      setBiodiversity(bio);
      setNews(nw);
      setIsLoading(false);
    });
  }, [selectedFarm]);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Agroclimate Insights & Multi-Source Data
          </h1>
          <p className="text-xs text-gray-600 mt-0.5">
            Explore satellite, meteorological, biodiversity, and outbreak news
            streams aggregated per farm plot.
          </p>
        </div>

        {farms.length > 0 && (
          <select
            value={selectedFarm?.id || ""}
            onChange={(e) =>
              setSelectedFarm(
                farms.find((f) => f.id === Number(e.target.value)) || null,
              )
            }
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm font-semibold"
          >
            {farms.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name} ({f.location_query})
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 space-x-2 overflow-x-auto">
        {(
          ["weather", "climate", "environment", "biodiversity", "news"] as const
        ).map((tab) => (
          <button
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2.5 text-xs font-bold uppercase tracking-wider border-b-2 transition-colors whitespace-nowrap ${
              activeTab === tab
                ? "border-emerald-700 text-emerald-800 bg-emerald-50/50"
                : "border-transparent text-gray-500 hover:text-gray-800"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="p-8 text-center bg-white rounded-xl border border-gray-200 shadow-sm text-gray-500 text-sm">
          Fetching multi-provider insight data streams...
        </div>
      ) : (
        <>
          {activeTab === "weather" && weather && (
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
              <h2 className="text-lg font-bold text-gray-900 border-b pb-3">
                Open-Meteo Live Weather & Forecast
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">Temperature:</span>{" "}
                  <strong className="text-sm block">
                    {weather.temperature_c}°C
                  </strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">Humidity:</span>{" "}
                  <strong className="text-sm block">
                    {weather.humidity_pct}%
                  </strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">Precipitation:</span>{" "}
                  <strong className="text-sm block">
                    {weather.rainfall_mm} mm
                  </strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">Soil Moisture:</span>{" "}
                  <strong className="text-sm block">
                    {weather.soil_moisture_m3m3} m³/m³
                  </strong>
                </div>
              </div>
            </div>
          )}

          {activeTab === "climate" && climate && (
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
              <h2 className="text-lg font-bold text-gray-900 border-b pb-3">
                NASA POWER Agroclimate Historical Baseline
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">30-Day Rain Total:</span>{" "}
                  <strong className="text-sm block">
                    {climate.total_precipitation_mm} mm
                  </strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">7-Day Rain Sum:</span>{" "}
                  <strong className="text-sm block">
                    {climate.rainfall_7d_mm} mm
                  </strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-gray-500">Consecutive Dry Days:</span>{" "}
                  <strong className="text-sm block">
                    {climate.dry_spell_days} days
                  </strong>
                </div>
              </div>
            </div>
          )}

          {activeTab === "environment" && (
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
              <h2 className="text-lg font-bold text-gray-900 border-b pb-3">
                Environment, Air Quality & Terrain Elevation
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                {airQuality && (
                  <div className="p-4 bg-slate-50 rounded-lg space-y-2 border">
                    <div className="font-bold text-slate-900">
                      OpenAQ Sensor Air Quality
                    </div>
                    <div>
                      PM2.5: <strong>{airQuality.pm25 ?? "--"} µg/m³</strong>
                    </div>
                    <div>
                      Estimated AQI:{" "}
                      <strong>{airQuality.aqi_estimate ?? "--"}</strong>
                    </div>
                  </div>
                )}
                {elevation && (
                  <div className="p-4 bg-slate-50 rounded-lg space-y-2 border">
                    <div className="font-bold text-slate-900">
                      Open Topo Data Relief
                    </div>
                    <div>
                      Terrain Elevation:{" "}
                      <strong>{elevation.elevation_m} meters</strong> above sea
                      level
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === "biodiversity" && biodiversity && (
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
              <h2 className="text-lg font-bold text-gray-900 border-b pb-3">
                GBIF Ecological & Species Observations
              </h2>
              <p className="text-xs text-gray-500">
                Total regional occurrences recorded:{" "}
                {biodiversity.total_observations}
              </p>
              <div className="space-y-2">
                {biodiversity.observations.map((b, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs flex justify-between"
                  >
                    <div>
                      <div className="font-bold text-slate-900">
                        {b.species_name}
                      </div>
                      <div className="text-slate-500">
                        {b.common_name || b.category}
                      </div>
                    </div>
                    <span className="bg-emerald-100 text-emerald-800 px-2 py-1 rounded font-mono text-[10px]">
                      Category: {b.category}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "news" && news && (
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
              <h2 className="text-lg font-bold text-gray-900 border-b pb-3">
                Agricultural Bulletins & Outbreak News
              </h2>
              <div className="space-y-3">
                {news.articles.map((art, idx) => (
                  <div
                    key={idx}
                    className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-1"
                  >
                    <div className="flex justify-between items-start">
                      <h3 className="font-bold text-slate-900 text-sm">
                        {art.title}
                      </h3>
                      <span className="text-[10px] bg-slate-200 px-2 py-0.5 rounded font-mono uppercase">
                        {art.category}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600">{art.summary}</p>
                    <div className="text-[11px] text-slate-400 pt-1">
                      Source: {art.source}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Insights;
