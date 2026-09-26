import type React from "react";
import { useEffect, useState } from "react";
import { CitationList } from "../components/CitationList";
import { RiskCard } from "../components/RiskCard";
import { farmService, soilService } from "../services/api";
import type { Farm, SoilAdviseResponse } from "../types";

export const Soil: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [selectedFarmId, setSelectedFarmId] = useState<number | undefined>(
    undefined,
  );

  const [nitrogen, setNitrogen] = useState<number>(40);
  const [phosphorus, setPhosphorus] = useState<number>(30);
  const [potassium, setPotassium] = useState<number>(20);
  const [ph, setPh] = useState<number>(6.5);
  const [moisture, setMoisture] = useState<number>(25);
  const [crop, setCrop] = useState<string>("Cotton");

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [result, setResult] = useState<SoilAdviseResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    farmService.listFarms().then((list) => {
      setFarms(list);
      if (list.length > 0) setSelectedFarmId(list[0].id);
    });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const res = await soilService.adviseSoil({
        nitrogen,
        phosphorus,
        potassium,
        ph,
        moisture,
        crop,
        farm_id: selectedFarmId,
      });
      setResult(res);
    } catch (err: unknown) {
      const msg =
        err instanceof Error
          ? err.message
          : "Failed to run soil health analysis.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">
          Soil Health Analysis & Advisory
        </h1>
        <p className="text-xs text-gray-600 mt-1">
          Input chemical & physical soil parameters (NPK, pH, Moisture) to
          trigger XGBoost model classification, environmental risk signals, and
          grounded RAG advisory.
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {farms.length > 0 && (
              <div>
                <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
                  Associate Farm Plot (Optional)
                </label>
                <select
                  value={selectedFarmId || ""}
                  onChange={(e) =>
                    setSelectedFarmId(
                      e.target.value ? Number(e.target.value) : undefined,
                    )
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="">-- Standalone / No Farm --</option>
                  {farms.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.name} ({f.primary_crop})
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
                Target Crop Type
              </label>
              <input
                type="text"
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                placeholder="e.g. Cotton, Rice"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <label className="block text-xs font-bold text-slate-700">
                Nitrogen (N)
              </label>
              <input
                type="number"
                min="0"
                max="200"
                value={nitrogen}
                onChange={(e) => setNitrogen(Number(e.target.value))}
                className="w-full mt-2 px-2 py-1.5 border rounded text-sm bg-white"
              />
              <span className="text-[10px] text-slate-400">0 - 200 mg/kg</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <label className="block text-xs font-bold text-slate-700">
                Phosphorus (P)
              </label>
              <input
                type="number"
                min="0"
                max="200"
                value={phosphorus}
                onChange={(e) => setPhosphorus(Number(e.target.value))}
                className="w-full mt-2 px-2 py-1.5 border rounded text-sm bg-white"
              />
              <span className="text-[10px] text-slate-400">0 - 200 mg/kg</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <label className="block text-xs font-bold text-slate-700">
                Potassium (K)
              </label>
              <input
                type="number"
                min="0"
                max="200"
                value={potassium}
                onChange={(e) => setPotassium(Number(e.target.value))}
                className="w-full mt-2 px-2 py-1.5 border rounded text-sm bg-white"
              />
              <span className="text-[10px] text-slate-400">0 - 200 mg/kg</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <label className="block text-xs font-bold text-slate-700">
                pH Level
              </label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="14"
                value={ph}
                onChange={(e) => setPh(Number(e.target.value))}
                className="w-full mt-2 px-2 py-1.5 border rounded text-sm bg-white"
              />
              <span className="text-[10px] text-slate-400">0.0 - 14.0 pH</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <label className="block text-xs font-bold text-slate-700">
                Moisture (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={moisture}
                onChange={(e) => setMoisture(Number(e.target.value))}
                className="w-full mt-2 px-2 py-1.5 border rounded text-sm bg-white"
              />
              <span className="text-[10px] text-slate-400">0 - 100 %</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="px-6 py-2.5 bg-emerald-700 text-white rounded-lg text-sm font-semibold hover:bg-emerald-800 shadow-sm disabled:opacity-50"
          >
            {isLoading ? "Analyzing Soil..." : "Run Soil Health Analysis"}
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs font-semibold">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* Result Card */}
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <div className="flex justify-between items-start border-b pb-3">
              <div>
                <div className="text-xs uppercase font-bold text-gray-400">
                  Predicted Soil Status
                </div>
                <h2 className="text-2xl font-black text-emerald-900 mt-1">
                  {result.predicted_category}
                </h2>
              </div>
              <div className="text-right">
                <span className="bg-amber-100 text-amber-900 text-xs font-bold px-2.5 py-1 rounded">
                  SYNTHETIC DEMO MODEL
                </span>
                <div className="text-[11px] text-gray-500 mt-1">
                  Confidence:{" "}
                  {result.confidence != null
                    ? `${(result.confidence * 100).toFixed(0)}%`
                    : "N/A (Uncalibrated)"}
                </div>
              </div>
            </div>

            <p className="text-xs text-amber-800 bg-amber-50 p-3 rounded-lg border border-amber-200">
              ⚠️ {result.limitation}
            </p>

            <div className="text-xs text-gray-500 font-mono flex gap-4">
              <span>Model: {result.model_provenance.model_name}</span>
              <span>Version: {result.model_provenance.model_version}</span>
            </div>
          </div>

          {/* Risk Card */}
          {result.risk_context && (
            <RiskCard riskContext={result.risk_context} />
          )}

          {/* Evidence Citations */}
          <CitationList citations={result.citations} />
        </div>
      )}
    </div>
  );
};

export default Soil;
