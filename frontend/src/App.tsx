import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import About from "./pages/About";
import Disease from "./pages/Disease";
import Home from "./pages/Home";
import ResponsibleAI from "./pages/ResponsibleAI";
import Soil from "./pages/Soil";
import "./i18n";

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Layout />}>
					<Route index element={<Home />} />
					<Route path="disease" element={<Disease />} />
					<Route path="soil" element={<Soil />} />
					<Route path="about" element={<About />} />
					<Route path="responsible-ai" element={<ResponsibleAI />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
}

export default App;
