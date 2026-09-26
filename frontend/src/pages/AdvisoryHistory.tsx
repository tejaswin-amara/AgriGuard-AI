import { useCallback, useEffect, useState } from "react";
import { CitationList } from "../components/CitationList";
import { advisoryService, farmService } from "../services/api";
import type { AdvisoryDetailResponse, Farm } from "../types";

export const AdvisoryHistory: React.FC = () => {
  const [advisories, setAdvisories] = useState<AdvisoryDetailResponse[]>([]);
  const [farms, setFarms] = useState<Farm[]>([]);
  const [selectedFarmId, setSelectedFarmId] = useState<number | undefined>(
    undefined,
  );
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const loadAdvisories = useCallback(async () => {
    setIsLoading(true);
    try {
      const list = await advisoryService.listAdvisories(selectedFarmId);
      setAdvisories(list);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [selectedFarmId]);

  useEffect(() => {
    farmService.listFarms().then(setFarms);
    loadAdvisories();
  }, [loadAdvisories]);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Advisory Audit Trail & History
          </h1>
          <p className="text-xs text-gray-600 mt-0.5">
            Complete audit trail of all generated grounded advisories with
            evidence citations and risk context.
          </p>
        </div>

        {farms.length > 0 && (
          <select
            value={selectedFarmId || ""}
            onChange={(e) =>
              setSelectedFarmId(
                e.target.value ? Number(e.target.value) : undefined,
              )
            }
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm font-semibold"
          >
            <option value="">All Farms</option>
            {farms.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name}
              </option>
            ))}
          </select>
        )}
      </div>

      {isLoading ? (
        <div className="p-8 text-center bg-white rounded-xl border border-gray-200 shadow-sm text-gray-500 text-sm">
          Loading advisory history...
        </div>
      ) : advisories.length === 0 ? (
        <div className="p-8 text-center bg-white rounded-xl border border-gray-200 shadow-sm text-gray-500 text-sm">
          No advisory history recorded yet. Run a Soil or Disease analysis to
          generate grounded advisories.
        </div>
      ) : (
        <div className="space-y-4">
          {advisories.map((adv) => (
            <div
              key={adv.id}
              className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-3"
            >
              <div className="flex justify-between items-center border-b pb-3 text-xs">
                <div className="flex items-center gap-2">
                  <span className="bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded uppercase">
                    {adv.source_type}
                  </span>
                  <span className="text-gray-500">Advisory #{adv.id}</span>
                </div>
                <div className="text-gray-400 font-mono">
                  {new Date(adv.created_at).toLocaleString()}
                </div>
              </div>

              <div className="text-sm text-gray-800 whitespace-pre-line bg-slate-50 p-4 rounded-lg border border-slate-200 font-sans">
                {adv.recommendation}
              </div>

              <CitationList citations={adv.citations} />

              <div className="text-[11px] text-gray-500 pt-2 flex justify-between items-center border-t">
                <span>LLM Provider: {adv.provider}</span>
                <span>Limitation: {adv.limitations}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AdvisoryHistory;
