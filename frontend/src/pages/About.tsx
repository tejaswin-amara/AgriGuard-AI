export default function About() {
	return (
		<div className="max-w-3xl mx-auto space-y-8">
			<h1 className="text-3xl font-bold text-green-800">About AgriGuard AI</h1>

			<section className="bg-white p-6 shadow rounded-lg border border-gray-200">
				<h2 className="text-2xl font-bold mb-4">The Problem</h2>
				<p className="text-gray-700">
					Smallholder farmers face avoidable crop loss due to late disease
					diagnosis and lack of contextual soil health advice. This leads to
					overuse of chemical inputs and diminished yields.
				</p>
			</section>

			<section className="bg-white p-6 shadow rounded-lg border border-gray-200">
				<h2 className="text-2xl font-bold mb-4">SDG Alignment</h2>
				<ul className="list-disc pl-5 text-gray-700 space-y-2">
					<li>
						<strong>SDG 2 (Zero Hunger):</strong> Primary focus. Protects
						farm-level food security.
					</li>
					<li>
						<strong>SDG 13 (Climate Action):</strong> Reduces climate-linked
						crop loss through optimized input.
					</li>
					<li>
						<strong>SDG 15 (Life on Land):</strong> Supports sustainable land
						use.
					</li>
				</ul>
			</section>

			<section className="bg-white p-6 shadow rounded-lg border border-gray-200">
				<h2 className="text-2xl font-bold mb-4">Target Users</h2>
				<p className="text-gray-700">
					Primary users are smallholder and marginal farmers. Secondary users
					include extension officers and agricultural cooperatives.
				</p>
			</section>
		</div>
	);
}
