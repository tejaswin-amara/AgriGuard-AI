# Demo Guide: AgriGuard AI

This document provides a clear path for evaluators to test the AgriGuard AI prototype.

## Starting the Application

The simplest way to run the application is using Docker:
```bash
docker compose up --build
```
Wait a few moments for the backend, database, and frontend to start.

- **Frontend Application:** Access via your browser at `http://localhost:80`
- **Backend API Docs:** Access via `http://localhost:8000/docs`

*Note: Before using the advisory features, ensure the demo corpus is ingested by running:*
```bash
python rag/ingestion/ingest.py
```

## Demo Path 1: Soil Health Advisory
1. Open the frontend and navigate to **Soil Health Advisory**.
2. Enter the following values (which represent sub-optimal pH and nutrient stress in our synthetic model):
   - Nitrogen: `40`
   - Phosphorus: `15`
   - Potassium: `20`
   - pH: `5.0`
   - Moisture: `25`
3. Click **Analyze Soil**.
4. **Observe the Results:**
   - The system displays a predicted category (e.g., "High Risk (pH imbalance)").
   - A limitation banner explicitly states this is a demo based on synthetic data.
   - The RAG system retrieves the document "Soil pH Management" (doc-002) and displays a grounded recommendation on managing acidic soil.

## Demo Path 2: Crop Disease Detection
1. Navigate to **Crop Disease Detection**.
2. Select a crop (e.g., "Tomato").
3. Upload any small image file (the model is in a deterministic demo mode, so the exact image content doesn't affect the mock output).
4. Click **Analyze Image**.
5. **Observe the Results:**
   - The system returns a mock "Leaf Blight" prediction with 85% confidence.
   - The limitation banner indicates this is a mock result.
   - The RAG system retrieves the document "Leaf Blight Management" (doc-001) and provides advice grounded in that source.

## Responsible AI Verification
1. Navigate to the **Responsible AI** page via the top menu.
2. Observe the explanations of Fairness, Transparency, Ethics, and Privacy.
3. Note the clear disclaimer regarding the prototype's limitations.
