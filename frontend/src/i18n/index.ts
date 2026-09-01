import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  en: {
    translation: {
      "home": "Home",
      "disease": "Disease",
      "soil": "Soil Advisory",
      "about": "About",
      "responsibleAI": "Responsible AI",
      "title": "AgriGuard AI",
      "subtitle": "AI-powered crop disease and soil health advisory for smallholder farmers.",
      // Adding placeholders to simulate architecture readiness
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: "en",
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
