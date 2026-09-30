# Model Card — Soil Health Classifier

> **Status:** Synthetic-data prototype; not field validated.

## Intended purpose

Demonstrate a tabular ML pipeline that accepts soil measurements, produces a categorical result, and feeds that result into the RAG advisory layer.

## Current implementation

- Framework: XGBoost
- Training script: `models/soil/train.py`
- Features: N, P, K, pH, moisture
- Synthetic samples generated: 1,000
- Training seed: 42
- Model file generated locally: `models/soil/soil_model_synthetic.pkl`
- Inference version string: `xgboost-synthetic-v1`

## Synthetic labels

The training script derives the target using heuristic rules.

Current labels:

1. `Optimal`
2. `High Risk (pH imbalance)`
3. `Suboptimal (Stress)`

These labels are demonstrations of the software pipeline, not laboratory classifications.

## Evaluation

No field or laboratory benchmark is available.

Model probabilities from XGBoost should not be presented as real-world confidence, agronomic certainty, or fertilizer-response probability.

## Missing-artifact behavior

If the generated model file is absent, the current inference implementation returns a deterministic fallback result. That fallback is part of the prototype behavior and is not a model prediction.

## Intended use

- demonstrating tabular classification;
- exercising the soil API;
- integrating model output with environmental context and RAG;
- deterministic prototype demonstrations.

## Out of scope

- fertilizer dosage recommendations;
- soil amendment prescriptions;
- laboratory soil diagnosis;
- agronomic certification;
- yield prediction.

## Production requirements

A production model would require real soil/lab observations, documented measurement units and procedures, representative geography and crops, train/validation/test separation, leakage checks, calibrated evaluation, and domain review.
