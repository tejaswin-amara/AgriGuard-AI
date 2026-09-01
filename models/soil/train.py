import numpy as np
import xgboost as xgb
import pickle
import os


def generate_synthetic_data(n_samples=1000, seed=42):
    """
    Generate synthetic soil data for demo purposes.
    Features: N, P, K, pH, Moisture
    """
    np.random.seed(seed)

    # Generate random features
    N = np.random.uniform(10, 150, n_samples)
    P = np.random.uniform(5, 80, n_samples)
    K = np.random.uniform(10, 100, n_samples)
    pH = np.random.uniform(4.5, 8.5, n_samples)
    moisture = np.random.uniform(10, 60, n_samples)

    X = np.column_stack((N, P, K, pH, moisture))

    # Generate target classes based on simple heuristic rules (for demo)
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if (
            6.0 <= pH[i] <= 7.5
            and N[i] > 50
            and P[i] > 20
            and K[i] > 30
            and moisture[i] > 30
        ):
            y[i] = 0  # Optimal
        elif pH[i] < 5.5 or pH[i] > 8.0:
            y[i] = 1  # High Risk (pH imbalance)
        else:
            y[i] = 2  # Suboptimal (Nutrient/Moisture stress)

    return X, y


def train_model():
    print("Generating synthetic data...")
    X, y = generate_synthetic_data()

    print("Training XGBoost model on synthetic data...")
    model = xgb.XGBClassifier(
        n_estimators=50, max_depth=3, random_state=42, eval_metric="mlogloss"
    )
    model.fit(X, y)

    # Save the model
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), "soil_model_synthetic.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Demo model saved to {model_path}")


if __name__ == "__main__":
    train_model()
