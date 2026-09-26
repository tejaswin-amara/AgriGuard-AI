import type React from "react";
import { useEffect, useState } from "react";
import { farmService, locationService } from "../services/api";
import type { Farm, GeocodedLocation } from "../types";

export const FarmSetup: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [name, setName] = useState("");
  const [locationQuery, setLocationQuery] = useState("");
  const [crop, setCrop] = useState("Cotton");
  const [plotId, setPlotId] = useState("");

  const [geocoded, setGeocoded] = useState<GeocodedLocation | null>(null);
  const [isGeocoding, setIsGeocoding] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  useEffect(() => {
    loadFarms();
  }, []);

  const loadFarms = async () => {
    try {
      const list = await farmService.listFarms();
      setFarms(list);
    } catch (err: unknown) {
      console.error("Failed to load farms", err);
    }
  };

  const handleGeocode = async () => {
    if (!locationQuery.trim()) return;
    setIsGeocoding(true);
    setMessage(null);
    try {
      const loc = await locationService.geocode(locationQuery);
      setGeocoded(loc);
    } catch (err: unknown) {
      const msg =
        err instanceof Error
          ? err.message
          : "Geocoding failed. Check location query.";
      setMessage({
        type: "error",
        text: msg,
      });
    } finally {
      setIsGeocoding(false);
    }
  };

  const handleCreateFarm = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !locationQuery) return;
    setIsSubmitting(true);
    setMessage(null);

    try {
      const farm = await farmService.createFarm({
        name,
        location_query: locationQuery,
        primary_crop: crop,
        plot_identifier: plotId || undefined,
      });
      setMessage({
        type: "success",
        text: `Farm '${farm.name}' created successfully!`,
      });
      setName("");
      setLocationQuery("");
      setPlotId("");
      setGeocoded(null);
      loadFarms();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to create farm.";
      setMessage({ type: "error", text: msg });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">
          Farm Setup & Location Onboarding
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          Register your farm plot with geographic location query. The system
          automatically resolves coordinates, elevation, and regional weather
          context.
        </p>

        {message && (
          <div
            className={`mt-4 p-3 rounded-lg text-xs font-semibold ${
              message.type === "success"
                ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                : "bg-rose-50 text-rose-800 border border-rose-200"
            }`}
          >
            {message.text}
          </div>
        )}

        <form onSubmit={handleCreateFarm} className="mt-6 space-y-4 max-w-2xl">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
                Farm Name *
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Nizamabad Cotton Field"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
                Primary Crop *
              </label>
              <select
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="Cotton">Cotton</option>
                <option value="Rice / Paddy">Rice / Paddy</option>
                <option value="Maize / Corn">Maize / Corn</option>
                <option value="Tomato">Tomato</option>
                <option value="Wheat">Wheat</option>
                <option value="Sugarcane">Sugarcane</option>
                <option value="General">General Crop</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
              Location / Village / District *
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={locationQuery}
                onChange={(e) => setLocationQuery(e.target.value)}
                placeholder="e.g. Nizamabad, Telangana, India"
                required
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
              <button
                type="button"
                onClick={handleGeocode}
                disabled={isGeocoding || !locationQuery}
                className="px-4 py-2 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-900 disabled:opacity-50"
              >
                {isGeocoding ? "Resolving..." : "Geocode"}
              </button>
            </div>
          </div>

          {geocoded && (
            <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-200 text-xs space-y-1">
              <div className="font-bold text-emerald-900">
                Resolved Location: {geocoded.display_name}
              </div>
              <div className="text-emerald-700 flex gap-4">
                <span>Latitude: {geocoded.latitude.toFixed(4)}°</span>
                <span>Longitude: {geocoded.longitude.toFixed(4)}°</span>
                {geocoded.state && <span>State: {geocoded.state}</span>}
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
              Plot / Survey Identifier (Optional)
            </label>
            <input
              type="text"
              value={plotId}
              onChange={(e) => setPlotId(e.target.value)}
              placeholder="e.g. Plot #14-B"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2.5 bg-emerald-700 text-white rounded-lg text-sm font-semibold hover:bg-emerald-800 shadow-sm disabled:opacity-50"
          >
            {isSubmitting ? "Creating Farm..." : "Save Farm Plot"}
          </button>
        </form>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <h2 className="text-lg font-bold text-gray-900 mb-4">
          Registered Farms ({farms.length})
        </h2>
        {farms.length === 0 ? (
          <p className="text-xs text-gray-500">
            No farms registered yet. Add a farm plot above.
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {farms.map((f) => (
              <div
                key={f.id}
                className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-slate-900 text-sm">
                      {f.name}
                    </h3>
                    <p className="text-xs text-slate-600">{f.location_query}</p>
                  </div>
                  <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded">
                    {f.primary_crop}
                  </span>
                </div>
                <div className="text-[11px] text-slate-500 flex gap-3 font-mono">
                  <span>Lat: {f.latitude.toFixed(2)}</span>
                  <span>Lon: {f.longitude.toFixed(2)}</span>
                  {f.plot_identifier && <span>Plot: {f.plot_identifier}</span>}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FarmSetup;
