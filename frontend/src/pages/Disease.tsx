import { useState } from "react";
import { analyzeDisease, generateAdvisory } from "../services/api";

export default function Disease() {
    const [crop, setCrop] = useState("tomato");
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [advisory, setAdvisory] = useState<any>(null);
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return setError("Please upload an image.");

        setLoading(true);
        setError("");
        setResult(null);
        setAdvisory(null);

        try {
            const analysis = await analyzeDisease(crop, file);
            setResult(analysis);

            const adv = await generateAdvisory("disease", analysis.id);
            setAdvisory(adv);
        } catch (err: any) {
            setError(err.response?.data?.detail || "An error occurred during analysis.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Disease Analysis</h1>
                <p className="text-gray-600 mt-2">Upload a leaf image to get an AI-powered risk assessment.</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 shadow rounded-lg border border-gray-200">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Crop</label>
                    <select value={crop} onChange={(e) => setCrop(e.target.value)} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border">
                        <option value="tomato">Tomato</option>
                        <option value="potato">Potato</option>
                        <option value="wheat">Wheat</option>
                    </select>
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Leaf Image</label>
                    <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100" />
                </div>
                <button type="submit" disabled={loading} className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50">
                    {loading ? "Analyzing..." : "Analyze Image"}
                </button>
            </form>

            {error && <div className="p-4 bg-red-50 text-red-700 rounded border border-red-200">{error}</div>}

            {result && (
                <div className="space-y-4">
                    <div className="bg-white p-6 shadow rounded-lg border border-gray-200">
                        <h2 className="text-xl font-bold mb-4">Analysis Result</h2>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div><span className="text-gray-500">Predicted Class:</span> <span className="font-semibold text-gray-900">{result.predicted_class}</span></div>
                            <div><span className="text-gray-500">Confidence:</span> <span className="font-semibold text-gray-900">{(result.confidence * 100).toFixed(1)}%</span></div>
                        </div>
                        {result.is_demo && (
                            <div className="mt-4 p-3 bg-yellow-50 text-yellow-800 rounded text-xs border border-yellow-200">
                                <strong>Limitation:</strong> {result.limitation}
                            </div>
                        )}
                    </div>

                    {advisory && (
                        <div className="bg-white p-6 shadow rounded-lg border border-gray-200">
                            <h2 className="text-xl font-bold mb-4">Advisory Recommendation</h2>
                            <p className="text-gray-800">{advisory.recommendation}</p>

                            {advisory.citations && advisory.citations.length > 0 && (
                                <div className="mt-6 border-t pt-4">
                                    <h3 className="text-sm font-bold text-gray-500 mb-2">Sources:</h3>
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
    )
}
