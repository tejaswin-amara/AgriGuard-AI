# AgriGuard AI

AI-powered crop disease and soil health advisory for smallholder Indian farmers.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Status:** Full Prototype Implemented. Backend (FastAPI), Frontend (React), ML Pipelines (Demo/Synthetic), and RAG Advisory are integrated and runnable locally.

Built for the **1M1B AI for Sustainability Virtual Internship**, in collaboration with IBM SkillsBuild and AICTE.

## The Problem
How might we use AI to give smallholder Indian farmers early, localized warning of crop disease risk and soil degradation — so that yield loss and overuse of chemical inputs can become more sustainable?

## SDG Alignment
- **SDG 2 — Zero Hunger** (Primary)
- **SDG 13 — Climate Action** (Secondary)
- **SDG 15 — Life on Land** (Secondary)

## Target Users
- **Primary:** Smallholder and marginal farmers.
- **Secondary:** Extension officers, NGOs, cooperatives.

## Features & AI Architecture
1. **Disease Pipeline (Prototype):** A PyTorch CNN structure (MobileNetV2). *Note: Currently runs in deterministic demo mode as no real dataset is present.*
2. **Soil Pipeline (Synthetic):** An XGBoost tabular model trained on synthetic data representing N-P-K, pH, and moisture.
3. **RAG Advisory:** A local vector database (ChromaDB) using `sentence-transformers` retrieves relevant agricultural advice from a demo corpus to ground LLM recommendations.
4. **IBM Granite Integration (Optional):** Provider abstraction allows using IBM Granite (via Watsonx) when credentials are provided, falling back to a local-demo provider.

## System Architecture
```text
Frontend (React + Tailwind)
   ↓
FastAPI (Backend)
   ↓
Disease (PyTorch Demo) / Soil (XGBoost) Inference
   ↓
RAG Retrieval (ChromaDB)
   ↓
LLM (Local Demo or IBM Granite)
   ↓
Grounded Advisory with Citations
   ↓
Frontend Display
```

## Responsible AI
- **Fairness:** Dataset limitations are audited and documented.
- **Transparency:** All outputs show confidence, model version, and explicit demo/synthetic limitations.
- **Ethics:** Tool is for decision support only. Fallbacks suggest consulting experts.
- **Privacy:** No unnecessary PII is collected.

## Limitations
- **Prototype Status:** The models are trained on synthetic data or run in demo mode. **They are not field-validated and must not be used for actual agricultural diagnosis or fertilizer dosing.**
- See [Dataset Card](docs/dataset-card/DATASET_CARD.md) and [Model Cards](docs/model-card/) for details.

## Project Structure
- `backend/`: FastAPI application.
- `frontend/`: React + Vite application.
- `models/`: PyTorch and XGBoost training/inference code.
- `rag/`: Corpus and vector DB scripts.
- `docs/`: Architecture and compliance documentation.

## Setup & Running Locally

### Using Docker (Recommended)
Use docker compose to start the services:
`docker compose up --build`
- Frontend: `http://localhost:80`
- Backend API Docs: `http://localhost:8000/docs`

### Manual Setup
1. **Backend:**
`cd backend && pip install -r requirements.txt && DATABASE_URL=sqlite:///./test.db uvicorn app.main:app --reload &`

2. **Frontend:**
`cd frontend && npm install && npm run start &`

3. **RAG Ingestion:**
To initialize the vector database for the demo corpus:
`python rag/ingestion/ingest.py`

## Testing
`cd backend && PYTHONPATH=. pytest tests/`

## Internship Compliance
See [`docs/INTERNSHIP-COMPLIANCE.md`](docs/INTERNSHIP-COMPLIANCE.md) for the full matrix mapping to 1M1B guidelines.

## License
MIT — see [`LICENSE`](LICENSE).
