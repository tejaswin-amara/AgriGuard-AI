# Model Card: Soil Health Advisory

**Status: Synthetic Data Trained**

## Purpose
To categorize soil health based on N, P, K, pH, and moisture readings.

## Architecture
XGBoost Classifier (`models/soil/train.py`).

## Training Data
**Synthetic Data**. Generated using basic heuristic rules (e.g., Optimal if pH is 6.0-7.5 and nutrients are high).

## Evaluation & Metrics
- The model learns the synthetic rules perfectly, but these metrics are **not real-world agricultural performance**.

## Intended Use
Demonstrating the tabular ML pipeline and integration with the RAG advisory layer.

## Out-of-Scope Use
Generating actual fertilizer prescriptions or agronomic advice.

## Responsible AI Considerations
The model output is explicitly marked as `is_synthetic` in the API, and the UI displays a warning that the results are not field-validated.
