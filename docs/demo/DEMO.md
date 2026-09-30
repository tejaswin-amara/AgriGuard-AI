# AgriGuard AI — Demo Guide

> **Demo type:** local software prototype  
> **Important:** Current disease inference is deterministic demo logic, soil inference is based on synthetic training data, and the RAG corpus is a three-document demo corpus.

## 1. Start the backend

### Backend dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Seed the RAG corpus

From the repository root:

```bash
python rag/ingestion/ingest.py
```

This creates a persistent ChromaDB collection under `rag/vector_db/` locally.

### Generate the synthetic soil model

```bash
python models/soil/train.py
```

This generates `models/soil/soil_model_synthetic.pkl`.

### Run the API

```bash
cd backend
DATABASE_URL=sqlite:///./demo.db PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

Open:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/api/v1/openapi.json`

## 2. Start the frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite serves the application on its normal development URL.

> The frontend API client uses a relative `/api/v1` base path. The repository currently does not define a Vite development proxy, so a full local browser flow requires the frontend and API to be served behind a compatible same-origin/reverse-proxy setup or the frontend API configuration to be adapted for local development.

## 3. Demo path — Farm context

1. Open the application.
2. Navigate to **Farms**.
3. Create a farm using a location query and primary crop.
4. Return to the dashboard.
5. Observe the farm context assembled from location, weather, climate, environmental providers, provider health, freshness state, and risk signals.

The live provider paths include Open-Meteo, NASA POWER, and Nominatim. Optional environment/biodiversity/news providers may be unavailable without preventing the farm-context response.

## 4. Demo path — Soil health

Use the Soil Health page and enter values such as:

```text
Nitrogen:   40
Phosphorus: 15
Potassium:  20
pH:         5.0
Moisture:   25
```

The current synthetic model is designed to classify this type of input as a high-risk/suboptimal category. The exact output depends on whether `soil_model_synthetic.pkl` has been generated.

The response should visibly carry the synthetic/prototype limitation.

## 5. Demo path — Crop disease

1. Open **Crop Disease**.
2. Select a crop label.
3. Upload a JPEG, PNG, or WebP image smaller than 10 MB.
4. Submit the analysis.

The current disease implementation validates the image and then returns a deterministic demo `Leaf Blight` result with a fixed demonstration confidence field. The image content does not drive a trained classifier.

## 6. Demo path — Grounded advisory

Advisories can be generated from:

- disease analysis;
- soil analysis;
- a general advisory query.

The RAG layer retrieves passages from the local corpus and attaches citations. When nothing is retrieved, the service returns an insufficient-evidence response rather than inventing an advisory.

IBM watsonx.ai / Granite is optional. Without valid `WATSONX_API_KEY` and `WATSONX_PROJECT_ID`, the local demo provider is used.

## 7. Responsible-AI checks

The application contains a **Responsible AI** page and surfaces provenance/limitation information.

Look for:

- provenance and source attribution;
- freshness labels;
- model/demo limitation messages;
- qualitative risk explanations;
- advisory citations.

## 8. Docker Compose

The repository also provides:

```bash
cp .env.example .env
docker compose up --build
```

Compose provisions PostgreSQL, MinIO, FastAPI, and the frontend container.

The Docker topology is useful for evaluating service composition, but the shipped frontend Nginx configuration currently does not provide an API reverse proxy to the backend. Treat this as a local infrastructure prototype rather than a production-ready deployment.
