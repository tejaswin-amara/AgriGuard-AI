import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

export default function Home() {
	const { t } = useTranslation();
	return (
		<div className="flex flex-col items-center justify-center space-y-8 text-center mt-12">
			<h1 className="text-4xl font-bold text-green-800">{t("title")}</h1>
			<p className="text-xl text-gray-600 max-w-2xl">{t("subtitle")}</p>

			<div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl mt-12">
				<Link
					to="/disease"
					className="p-8 bg-white shadow rounded-lg border border-gray-200 hover:border-green-500 transition"
				>
					<h2 className="text-2xl font-semibold mb-2">
						Crop Disease Detection
					</h2>
					<p className="text-gray-500">
						Upload a photo of a crop leaf for early disease risk warning and
						grounded advisory.
					</p>
				</Link>
				<Link
					to="/soil"
					className="p-8 bg-white shadow rounded-lg border border-gray-200 hover:border-green-500 transition"
				>
					<h2 className="text-2xl font-semibold mb-2">Soil Health Advisory</h2>
					<p className="text-gray-500">
						Input N-P-K, pH, and moisture readings to get a soil health
						assessment and recommendations.
					</p>
				</Link>
			</div>

			<div className="mt-12 p-4 bg-blue-50 text-blue-800 rounded max-w-3xl text-sm text-left border border-blue-200">
				<strong>Prototype Notice:</strong> This application is a demonstration
				prototype. AI models are trained on synthetic or demo data and outputs
				are NOT field-validated. Please see the{" "}
				<Link to="/responsible-ai" className="underline">
					Responsible AI
				</Link>{" "}
				section.
			</div>
		</div>
	);
}
