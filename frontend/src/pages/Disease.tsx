import { useEffect, useState } from "react";
import { CitationList } from "../components/CitationList";
import { RiskCard } from "../components/RiskCard";
import { diseaseService, farmService } from "../services/api";
import type { DiseaseAnalyzeResponse, Farm } from "../types";

export const Disease: React.FC = () => {
  const [farms, setFarms] = useState<Farm[]>([]);
  const [selectedFarmId, setSelectedFarmId] = useState<number | undefined>(undefined);
  const [crop, setCrop] = useState<string>("Tomato");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [result, setResult] = useState<DiseaseAnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    farmService.listFarms().then((list) => {
      setFarms(list);
      if (list.length > 0) setSelectedFarmId(list[0].id);
    });
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setError("Please select a leaf image file to upload.");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const res = await diseaseService.analyzeDisease(selectedFile, crop, selectedFarmId);
      setResult(res);
    } catch (err: any) {
      setError("Failed to analyze crop leaf image.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">Crop Leaf Disease Inference</h1>
        <p className="text-xs text-gray-600 mt-1">
          Upload a crop leaf image for PyTorch CNN disease classification, environmental fungal pressure assessment,
          and grounded RAG treatment advisory.
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {farms.length > 0 && (
              <div>
                <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">
                  Associate Farm Plot (Optional)
                </label>
                <select
                  value={selectedFarmId || ""}
                  onChange={(e) => setSelectedFarmId(e.target.value ? Number(e.target.value) : undefined)}
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
              <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">Crop Type *</label>
              <input
                type="text"
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                placeholder="e.g. Tomato, Cotton, Rice"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase mb-1">Leaf Image File *</label>
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer relative">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              {previewUrl ? (
                <div className="flex flex-col items-center gap-2">
                  <img src={previewUrl} alt="Leaf Preview" className="h-32 object-contain rounded-lg shadow-sm" />
                  <span className="text-xs text-gray-600 font-semibold">{selectedFile?.name}</span>
                </div>
              ) : (
                <div className="space-y-1">
                  <div className="text-3xl">🍃</div>
                  <div className="text-sm font-semibold text-gray-700">Click or drag crop leaf photo here</div>
                  <div className="text-xs text-gray-400">Supports JPEG, PNG up to 10MB</div>
                </div>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading || !selectedFile}
            className="px-6 py-2.5 bg-emerald-700 text-white rounded-lg text-sm font-semibold hover:bg-emerald-800 shadow-sm disabled:opacity-50"
          >
            {isLoading ? "Running Disease Inference..." : "Analyze Crop Disease"}
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
          <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
            <div className="flex justify-between items-start border-b pb-3">
              <div>
                <div className="text-xs uppercase font-bold text-gray-400">Predicted Disease / Health Status</div>
                <h2 className="text-2xl font-black text-emerald-900 mt-1">{result.predicted_class}</h2>
              </div>
              <div className="text-right">
                <span className="bg-blue-100 text-blue-900 text-xs font-bold px-2.5 py-1 rounded">
                  DEMO MODEL
                </span>
                <div className="text-[11px] text-gray-500 mt-1">
                  Confidence: {(result.confidence * 100).toFixed(0)}%
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

          {result.risk_context && <RiskCard riskContext={result.risk_context} />}

          <CitationList citations={result.citations} />
        </div>
      )}
    </div>
  );
};

export default Disease;
