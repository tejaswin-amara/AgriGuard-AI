export default function ResponsibleAI() {
	return (
		<div className="max-w-3xl mx-auto space-y-8">
			<h1 className="text-3xl font-bold text-green-800">
				Responsible AI Guidelines
			</h1>

			<section className="bg-white p-6 shadow rounded-lg border border-gray-200">
				<h2 className="text-2xl font-bold mb-4">Core Pillars</h2>
				<div className="space-y-4 text-gray-700">
					<div>
						<h3 className="font-bold text-gray-900">Fairness</h3>
						<p>
							We commit to auditing dataset composition by crop and region
							before field deployment to avoid representational bias.
						</p>
					</div>
					<div>
						<h3 className="font-bold text-gray-900">Transparency</h3>
						<p>
							Every recommendation explicitly shows its source citation and
							model confidence. Demo results are clearly labeled.
						</p>
					</div>
					<div>
						<h3 className="font-bold text-gray-900">Ethics</h3>
						<p>
							This tool provides decision support, not definitive diagnoses.
							Users are advised to consult agronomists for critical issues.
						</p>
					</div>
					<div>
						<h3 className="font-bold text-gray-900">Privacy</h3>
						<p>
							Data minimization is applied. We do not collect unnecessary farmer
							PII (names, phone numbers) for core model function.
						</p>
					</div>
				</div>
			</section>

			<section className="bg-yellow-50 p-6 shadow rounded-lg border border-yellow-200 text-yellow-800">
				<h2 className="text-xl font-bold mb-2">Prototype Limitations</h2>
				<p>
					The current implementation is a <strong>demo prototype</strong>. The
					disease detection uses a structural stub, the soil model is trained on
					synthetic data, and the RAG corpus uses a limited set of demo
					documents.
					<strong>
						Outputs must not be used for actual agricultural decision-making.
					</strong>
				</p>
			</section>
		</div>
	);
}
