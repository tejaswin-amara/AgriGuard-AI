# Dataset Card: AgriGuard Demo

**Status: Synthetic / Demo**

## Overview
Currently, AgriGuard AI is a functional prototype. It does **not** yet use a real, field-validated agricultural dataset.
The system is built to support two types of datasets in the future:
1. **Crop Disease Images**: For the disease classification model.
2. **Soil Health Readings**: Tabular data for the soil advisory model.

### Current Demo Data
- **Disease Model**: Uses deterministic demo rules for inference rather than a trained model. It does not use real images for training.
- **Soil Model**: Uses **synthetic data** generated via a heuristic Python script (`models/soil/train.py`). The synthetic data simulates ranges of Nitrogen, Phosphorus, Potassium, pH, and Moisture to categorize soil into "Optimal", "High Risk", or "Suboptimal".

## Limitations
- **No Field Validation**: The synthetic soil data does not represent actual agronomic truth and must not be used to make real fertilizer dosage claims.
- **Demo Purposes Only**: The current datasets (or lack thereof) are purely to demonstrate the end-to-end technical pipeline (UI -> API -> Inference -> RAG -> UI).
