import type React from "react";

export const About: React.FC = () => {
	return (
		<div className="space-y-6">
			<div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-4">
				<h1 className="text-2xl font-bold text-gray-900">
					About AgriGuard AI Platform
				</h1>
				<p className="text-sm text-gray-600">
					Built for the 1M1B AI for Sustainability Virtual Internship (with IBM
					SkillsBuild & AICTE).
				</p>

				<div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200 space-y-2 text-xs text-emerald-900">
					<div className="font-bold text-sm">System Architecture Overview</div>
					<p>
						AgriGuard AI integrates PyTorch CNN leaf disease inference, XGBoost
						soil classification, Open-Meteo live weather, NASA POWER 30-day
						agroclimate baselines, Nominatim geocoding, OpenAQ air quality, Open
						Topo Data relief, GBIF biodiversity observations, ChromaDB RAG, and
						IBM Granite LLM reasoning into an integrated agricultural
						intelligence platform.
					</p>
				</div>

				<div className="space-y-2">
					<h2 className="text-base font-bold text-gray-900">
						Integrated Public API Catalog Matrix
					</h2>
					<div className="overflow-x-auto">
						<table className="w-full text-xs text-left text-gray-600 border border-gray-200">
							<thead className="bg-slate-100 text-gray-800 font-bold uppercase text-[10px]">
								<tr>
									<th className="p-2.5 border-b">Provider</th>
									<th className="p-2.5 border-b">Capability</th>
									<th className="p-2.5 border-b">Type</th>
									<th className="p-2.5 border-b">Cache Policy</th>
									<th className="p-2.5 border-b">Attribution</th>
								</tr>
							</thead>
							<tbody className="divide-y divide-gray-100">
								<tr>
									<td className="p-2.5 font-bold">Open-Meteo</td>
									<td className="p-2.5">
										Weather, ET0, VPD, Soil Temp/Moisture
									</td>
									<td className="p-2.5">Core (Required)</td>
									<td className="p-2.5 font-mono">30 mins</td>
									<td className="p-2.5">Open-Meteo.com</td>
								</tr>
								<tr>
									<td className="p-2.5 font-bold">NASA POWER</td>
									<td className="p-2.5">30-Day Agroclimate, Rain, GDD</td>
									<td className="p-2.5">Core (Required)</td>
									<td className="p-2.5 font-mono">24 hours</td>
									<td className="p-2.5">NASA POWER Program</td>
								</tr>
								<tr>
									<td className="p-2.5 font-bold">Nominatim OSM</td>
									<td className="p-2.5">Forward & Reverse Geocoding</td>
									<td className="p-2.5">Core (Required)</td>
									<td className="p-2.5 font-mono">7 days</td>
									<td className="p-2.5">OpenStreetMap Contributors</td>
								</tr>
								<tr>
									<td className="p-2.5 font-bold">OpenAQ</td>
									<td className="p-2.5">Environmental Air Quality</td>
									<td className="p-2.5">Optional</td>
									<td className="p-2.5 font-mono">1 hour</td>
									<td className="p-2.5">OpenAQ Community</td>
								</tr>
								<tr>
									<td className="p-2.5 font-bold">Open Topo Data</td>
									<td className="p-2.5">Terrain Relief Elevation</td>
									<td className="p-2.5">Optional</td>
									<td className="p-2.5 font-mono">7 days</td>
									<td className="p-2.5">ETOPO1 Global Relief Model</td>
								</tr>
								<tr>
									<td className="p-2.5 font-bold">GBIF</td>
									<td className="p-2.5">Biodiversity & Species Occurrences</td>
									<td className="p-2.5">Optional</td>
									<td className="p-2.5 font-mono">24 hours</td>
									<td className="p-2.5">GBIF Facility</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	);
};

export default About;
