import { useState } from "react";
import { adviseSoil, generateAdvisory } from "../services/api";

export default function Soil() {
	const [formData, setFormData] = useState({
		nitrogen: 50,
		phosphorus: 30,
		potassium: 40,
		ph: 6.5,
		moisture: 35,
	});
	const [loading, setLoading] = useState(false);
	const [result, setResult] = useState<any>(null);
	const [advisory, setAdvisory] = useState<any>(null);
	const [error, setError] = useState("");

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setFormData({
			...formData,
			[e.target.name]: Number.parseFloat(e.target.value),
		});
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setLoading(true);
		setError("");
		setResult(null);
		setAdvisory(null);

		try {
			const analysis = await adviseSoil(formData);
			setResult(analysis);

			const adv = await generateAdvisory("soil", analysis.id);
			setAdvisory(adv);
		} catch (err: any) {
			setError(
				err.response?.data?.detail || "An error occurred during analysis.",
			);
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="max-w-2xl mx-auto space-y-8">
			<div>
				<h1 className="text-3xl font-bold text-gray-900">
					Soil Health Advisory
				</h1>
				<p className="text-gray-600 mt-2">
					Enter soil parameters to get an AI-powered assessment.
				</p>
			</div>

			<form
				onSubmit={handleSubmit}
				className="bg-white p-6 shadow rounded-lg border border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-4"
			>
				{Object.keys(formData).map((key) => (
					<div key={key}>
						<label className="block text-sm font-medium text-gray-700 capitalize">
							{key}
						</label>
						<input
							type="number"
							name={key}
							step="0.1"
							value={formData[key as keyof typeof formData]}
							onChange={handleChange}
							required
							className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
						/>
					</div>
				))}

				<div className="md:col-span-2 pt-4">
					<button
						type="submit"
						disabled={loading}
						className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
					>
						{loading ? "Analyzing..." : "Analyze Soil"}
					</button>
				</div>
			</form>

			{error && (
				<div className="p-4 bg-red-50 text-red-700 rounded border border-red-200">
					{error}
				</div>
			)}

			{result && (
				<div className="space-y-4">
					<div className="bg-white p-6 shadow rounded-lg border border-gray-200">
						<h2 className="text-xl font-bold mb-4">Assessment Result</h2>
						<div className="grid grid-cols-2 gap-4 text-sm">
							<div>
								<span className="text-gray-500">Predicted Category:</span>{" "}
								<span className="font-semibold text-gray-900">
									{result.predicted_category}
								</span>
							</div>
							<div>
								<span className="text-gray-500">Confidence:</span>{" "}
								<span className="font-semibold text-gray-900">
									{(result.confidence * 100).toFixed(1)}%
								</span>
							</div>
						</div>
						{result.is_synthetic && (
							<div className="mt-4 p-3 bg-yellow-50 text-yellow-800 rounded text-xs border border-yellow-200">
								<strong>Limitation:</strong> {result.limitation}
							</div>
						)}
					</div>

					{advisory && (
						<div className="bg-white p-6 shadow rounded-lg border border-gray-200">
							<h2 className="text-xl font-bold mb-4">
								Advisory Recommendation
							</h2>
							<p className="text-gray-800">{advisory.recommendation}</p>

							{advisory.citations && advisory.citations.length > 0 && (
								<div className="mt-6 border-t pt-4">
									<h3 className="text-sm font-bold text-gray-500 mb-2">
										Sources:
									</h3>
									<ul className="space-y-2 text-sm text-gray-600">
										{advisory.citations.map((c: any, i: number) => (
											<li key={i} className="bg-gray-50 p-2 rounded">
												<strong>{c.title}</strong> ({c.organization})
											</li>
										))}
									</ul>
								</div>
							)}
						</div>
					)}
				</div>
			)}
		</div>
	);
}
