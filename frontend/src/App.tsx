import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import About from "./pages/About";
import AdvisoryHistory from "./pages/AdvisoryHistory";
import Dashboard from "./pages/Dashboard";
import Disease from "./pages/Disease";
import FarmSetup from "./pages/FarmSetup";
import Insights from "./pages/Insights";
import ResponsibleAI from "./pages/ResponsibleAI";
import Soil from "./pages/Soil";
import "./i18n";

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Layout />}>
					<Route index element={<Dashboard />} />
					<Route path="farm" element={<FarmSetup />} />
					<Route path="soil" element={<Soil />} />
					<Route path="disease" element={<Disease />} />
					<Route path="insights" element={<Insights />} />
					<Route path="history" element={<AdvisoryHistory />} />
					<Route path="responsible-ai" element={<ResponsibleAI />} />
					<Route path="about" element={<About />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
}

export default App;
