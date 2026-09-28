import type React from "react";
import { useTranslation } from "react-i18next";
import { Link, NavLink, Outlet } from "react-router-dom";

export const Layout: React.FC = () => {
	const { i18n } = useTranslation();

	const changeLanguage = (lng: string) => {
		i18n.changeLanguage(lng);
	};

	const navClass = ({ isActive }: { isActive: boolean }) =>
		`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
			isActive
				? "bg-emerald-700 text-white font-semibold"
				: "text-emerald-100 hover:bg-emerald-800 hover:text-white"
		}`;

	return (
		<div className="min-h-screen bg-slate-50 flex flex-col font-sans">
			<header className="bg-emerald-900 text-white shadow-md sticky top-0 z-50">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
					<div className="flex items-center justify-between h-16">
						<div className="flex items-center gap-3">
							<Link
								to="/"
								className="flex items-center gap-2 font-bold text-xl text-white"
							>
								<span className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-white font-black">
									🌱
								</span>
								<span>AgriGuard AI</span>
							</Link>
							<span className="hidden sm:inline-block text-xs bg-emerald-800 text-emerald-200 px-2 py-0.5 rounded font-mono">
								v2.0 Platform
							</span>
						</div>

						<nav className="hidden md:flex items-center space-x-1">
							<NavLink to="/" end className={navClass}>
								Dashboard
							</NavLink>
							<NavLink to="/farm" className={navClass}>
								Farms
							</NavLink>
							<NavLink to="/soil" className={navClass}>
								Soil Health
							</NavLink>
							<NavLink to="/disease" className={navClass}>
								Crop Disease
							</NavLink>
							<NavLink to="/insights" className={navClass}>
								Insights & Data
							</NavLink>
							<NavLink to="/history" className={navClass}>
								Advisory History
							</NavLink>
							<NavLink to="/responsible-ai" className={navClass}>
								Responsible AI
							</NavLink>
							<NavLink to="/about" className={navClass}>
								About
							</NavLink>
						</nav>

						<div className="flex items-center gap-2">
							<select
								onChange={(e) => changeLanguage(e.target.value)}
								value={i18n.language}
								className="bg-emerald-800 text-emerald-100 text-xs rounded-md px-2 py-1.5 border border-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-400"
							>
								<option value="en">English</option>
								<option value="hi">हिंदी (Hindi)</option>
								<option value="te">తెలుగు (Telugu)</option>
							</select>
						</div>
					</div>
				</div>
			</header>

			<main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
				<Outlet />
			</main>

			<footer className="bg-white border-t border-slate-200 py-6 text-xs text-slate-500 mt-auto">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
					<div>
						&copy; 2026 AgriGuard AI — Context-Aware Agricultural Intelligence &
						Decision Support
					</div>
					<div className="flex items-center gap-4 text-slate-600">
						<span>
							Powered by Open-Meteo • NASA POWER • OpenStreetMap • IBM WatsonX
						</span>
					</div>
				</div>
			</footer>
		</div>
	);
};

export default Layout;
