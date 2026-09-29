import type React from "react";
import type { RiskContext } from "../types";

interface Props {
	riskContext?: RiskContext;
}

export const RiskCard: React.FC<Props> = ({ riskContext }) => {
	if (!riskContext) return null;

	const getLevelColor = (level: string) => {
		switch (level.toLowerCase()) {
			case "elevated":
			case "severe":
			case "high":
				return "bg-rose-50 text-rose-800 border-rose-200";
			case "moderate":
			case "mild":
				return "bg-amber-50 text-amber-800 border-amber-200";
			default:
				return "bg-emerald-50 text-emerald-800 border-emerald-200";
		}
	};

	return (
		<div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-4">
			<div className="flex items-center justify-between border-b pb-3">
				<h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
					<span className="w-2.5 h-2.5 rounded-full bg-emerald-600" />
					Agronomic Risk & Context Indicators
				</h3>
				<span
					className={`px-3 py-1 rounded-full text-xs font-semibold border ${getLevelColor(
						riskContext.overall_level,
					)}`}
				>
					Overall: {riskContext.overall_level.toUpperCase()}
				</span>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-3 gap-3">
				<div
					className={`p-3 rounded-lg border ${getLevelColor(riskContext.fungal_pressure)}`}
				>
					<div className="text-xs font-medium uppercase tracking-wide opacity-75">
						Fungal Pressure
					</div>
					<div className="text-sm font-bold capitalize mt-1">
						{riskContext.fungal_pressure}
					</div>
				</div>

				<div
					className={`p-3 rounded-lg border ${getLevelColor(riskContext.water_stress)}`}
				>
					<div className="text-xs font-medium uppercase tracking-wide opacity-75">
						Water Stress
					</div>
					<div className="text-sm font-bold capitalize mt-1">
						{riskContext.water_stress}
					</div>
				</div>

				<div
					className={`p-3 rounded-lg border ${getLevelColor(riskContext.heat_stress)}`}
				>
					<div className="text-xs font-medium uppercase tracking-wide opacity-75">
						Heat Stress
					</div>
					<div className="text-sm font-bold capitalize mt-1">
						{riskContext.heat_stress}
					</div>
				</div>
			</div>

			{riskContext.explanations && riskContext.explanations.length > 0 && (
				<div className="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-100 space-y-1">
					<div className="font-semibold text-gray-700">Context Drivers:</div>
					<ul className="list-disc list-inside space-y-0.5">
						{riskContext.explanations.map((exp, idx) => (
							<li key={idx}>{exp}</li>
						))}
					</ul>
				</div>
			)}
		</div>
	);
};
