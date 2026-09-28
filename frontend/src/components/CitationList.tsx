import type React from "react";
import type { Citation } from "../types";

interface Props {
  citations?: Citation[];
}

export const CitationList: React.FC<Props> = ({ citations }) => {
  if (!citations || citations.length === 0) return null;

  return (
    <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
      <h4 className="text-sm font-bold text-gray-900 flex items-center gap-2">
        <svg
          className="w-4 h-4 text-emerald-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
          />
        </svg>
        Evidence Citations & Source Provenance
      </h4>
      <div className="space-y-2">
        {citations.map((cite, idx) => (
          <div
            key={idx}
            className="p-3 bg-gray-50 rounded-lg border border-gray-100 text-xs space-y-1"
          >
            <div className="flex items-center justify-between">
              <span className="font-bold text-gray-800">{cite.title}</span>
              <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-mono text-[10px]">
                {cite.organization}
              </span>
            </div>
            <p className="text-gray-600 italic">"{cite.content}"</p>
            {cite.url && (
              <a
                href={cite.url}
                target="_blank"
                rel="noreferrer"
                className="inline-block text-emerald-600 font-medium hover:underline text-[11px]"
              >
                View Official Source Directive &rarr;
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
