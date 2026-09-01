import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Disease from "./pages/Disease";
import Soil from "./pages/Soil";
import About from "./pages/About";
import ResponsibleAI from "./pages/ResponsibleAI";
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
