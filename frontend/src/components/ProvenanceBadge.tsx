import type React from "react";

interface Props {
	provider?: string;
	quality?: string;
}

export const ProvenanceBadge: React.FC<Props> = ({ provider, quality }) => {
	return (
		<div className="inline-flex items-center gap-1.5 text-xs text-gray-600 bg-gray-50 px-2 py-1 rounded border border-gray-200">
			<span className="font-semibold text-gray-700">
				{provider || "AgriGuard Engine"}
			</span>
			{quality && (
				<>
					<span className="text-gray-300">•</span>
					<span className="text-gray-500 font-mono text-[10px] uppercase">
						{quality}
					</span>
				</>
			)}
		</div>
	);
};
