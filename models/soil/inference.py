import pickle
import numpy as np
import os


class SoilInference:
    def __init__(self):
        self.version = "xgboost-synthetic-v1"
        self.is_synthetic = True
        self.classes = ["Optimal", "High Risk (pH imbalance)", "Suboptimal (Stress)"]

        model_path = os.path.join(os.path.dirname(__file__), "soil_model_synthetic.pkl")
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            self.model = None

    def predict(self, n: float, p: float, k: float, ph: float, moisture: float) -> dict:
        """Predict soil category using synthetic-trained model."""
        if self.model is None:
            # Fallback if model file isn't generated
            return {
                "category": "Optimal",
                "confidence": 0.99,
                "version": self.version,
                "is_synthetic": self.is_synthetic,
                "limitation": "Model not loaded. Demo fallback.",
            }

        features = np.array([[n, p, k, ph, moisture]])
        probs = self.model.predict_proba(features)[0]
        class_idx = np.argmax(probs)

        return {
            "category": self.classes[class_idx],
            "confidence": float(probs[class_idx]),
            "version": self.version,
            "is_synthetic": self.is_synthetic,
            "limitation": "Trained on synthetic data. Not field validated.",
        }
