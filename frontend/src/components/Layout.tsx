import { Link, Outlet } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Leaf } from "lucide-react";

export default function Layout() {
    const { t } = useTranslation();
    return (
        <div className="min-h-screen flex flex-col">
            <header className="bg-green-700 text-white shadow">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-2 font-bold text-xl">
                        <Leaf />
                        <span>{t('title')}</span>
                    </Link>
                    <nav className="flex space-x-4">
                        <Link to="/disease" className="hover:text-green-200">{t('disease')}</Link>
                        <Link to="/soil" className="hover:text-green-200">{t('soil')}</Link>
                        <Link to="/responsible-ai" className="hover:text-green-200">{t('responsibleAI')}</Link>
                        <Link to="/about" className="hover:text-green-200">{t('about')}</Link>
                    </nav>
                </div>
            </header>
            <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
                <Outlet />
            </main>
            <footer className="bg-gray-800 text-white py-6 text-center text-sm">
                <p>AgriGuard AI - 1M1B AI for Sustainability Virtual Internship Prototype</p>
                <p className="text-gray-400 mt-2">Not field validated. Consult agricultural experts for actual recommendations.</p>
            </footer>
        </div>
    )
}
