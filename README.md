# 🌱 AgriGuard AI

### Context-aware agricultural intelligence & advisory prototype

[![CI/CD](https://github.com/tejaswin-amara/AgriGuard-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/tejaswin-amara/AgriGuard-AI/actions/workflows/ci.yml)
[![Docker Build & Scan](https://github.com/tejaswin-amara/AgriGuard-AI/actions/workflows/docker-build.yml/badge.svg)](https://github.com/tejaswin-amara/AgriGuard-AI/actions/workflows/docker-build.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Node.js 22](https://img.shields.io/badge/Node.js-22+-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=111111)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Prototype status:** AgriGuard AI is a working software prototype, not a field-validated agricultural diagnostic system. The current disease model is deterministic demo inference, the soil model is trained on synthetic data when generated locally, the RAG corpus contains three demo documents, and some external-provider paths include deterministic fallback behavior.

AgriGuard AI is a full-stack decision-support prototype for crop and soil monitoring. It combines farm location, weather, historical climate, environmental context, machine-learning demonstrations, qualitative risk signals, and retrieval-augmented advisory generation behind a React interface and FastAPI API.

The project is organized as a single repository with a Python backend, React frontend, model code, RAG ingestion/retrieval code, Docker Compose infrastructure, and GitHub Actions validation.

---

## ✨ What it does

| Capability | What is implemented |
|---|---|
| **Farm context** | Creates farms from a location query and aggregates geocoded location, weather, climate, environment, biodiversity, news, provider health, freshness, and risk context. |
| **Crop disease demo** | Accepts JPEG, PNG, or WebP images up to 10 MB and returns deterministic demo output from the current MobileNetV2-based prototype contract. |
| **Soil health demo** | Accepts nitrogen, phosphorus, potassium, pH, and moisture values and classifies them with an XGBoost model trained from synthetic heuristic data when the generated model artifact exists. |
| **Grounded advisory** | Retrieves passages from the local ChromaDB corpus and sends the retrieved context to either the local demo provider or IBM watsonx.ai / Granite when configured. |
| **Environmental intelligence** | Pulls weather, historical agroclimate, air quality, elevation, biodiversity, and geocoding data through provider adapters. |
| **Risk signals** | Produces qualitative fungal-pressure, water-stress, and heat-stress indicators from available weather/climate inputs. |
| **Auditability** | Persists farm, observation, ML-analysis, and advisory records in PostgreSQL/SQLModel and exposes advisory history APIs. |

---

## 🧭 Architecture

```mermaid
flowchart TD
    UI["React + Vite Frontend"] --> API["FastAPI REST API"]

    API --> FARM["Farm & Location Services"]
    API --> ML["ML Services"]
    API --> RISK["Risk Engine"]
    API --> RAG["RAG Service"]
    API --> PROVIDERS["External Provider Layer"]
    API --> DB["PostgreSQL"]

    ML --> DISEASE["MobileNetV2 Demo Inference"]
    ML --> SOIL["XGBoost Synthetic Soil Model"]

    RAG --> CHROMA["ChromaDB"]
    RAG --> EMB["Sentence Transformers"]
    RAG --> LLM["IBM watsonx.ai / Granite or Local Demo"]

    PROVIDERS --> METEO["Open-Meteo"]
    PROVIDERS --> NASA["NASA POWER"]
    PROVIDERS --> NOM["Nominatim / OpenStreetMap"]
    PROVIDERS --> AQ["OpenAQ"]
    PROVIDERS --> TOPO["Open Topo Data"]
    PROVIDERS --> GBIF["GBIF"]
    PROVIDERS --> NEWS["Curated Agricultural News Provider"]

    API -. optional image-storage integration .-> MINIO["MinIO"]
```

### Request flow

1. A user configures a farm or submits a soil value or leaf image.
2. FastAPI validates the request and persists the relevant record.
3. Farm context requests external data concurrently and attaches freshness/provenance metadata.
4. The risk engine derives qualitative environmental signals.
5. Disease/soil analysis can trigger RAG retrieval for supporting advisory context.
6. The advisory service refuses to fabricate an answer when no corpus evidence is retrieved.
7. A local deterministic provider is used by default; IBM Granite can be used when watsonx.ai credentials are configured.

---

## 🧱 Repository structure

```text
AgriGuard-AI/
├── backend/
│   ├── app/
│   │   ├── api/routes/        # REST endpoints
│   │   ├── core/              # configuration
│   │   ├── db/                # SQLModel session
│   │   ├── models/            # database models
│   │   ├── schemas/           # API contracts
│   │   └── services/
│   │       ├── external/      # provider adapters, cache, registry
│   │       ├── disease.py
│   │       ├── farm_context.py
│   │       ├── llm.py
│   │       ├── rag.py
│   │       ├── risk_engine.py
│   │       └── soil.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── tests/e2e/
│   ├── Dockerfile
│   └── package.json
├── models/
│   ├── disease/               # MobileNetV2 demo architecture/inference
│   └── soil/                  # synthetic-data XGBoost pipeline
├── rag/
│   ├── corpus/                # demo advisory documents
│   ├── ingestion/             # ChromaDB ingestion
│   └── retrieval/             # semantic retrieval
├── docs/
├── docker-compose.yml
├── .env.example
├── AGENTS.md
├── CHANGELOG.md
├── DATA_AND_MODELS.md
├── SECURITY.md
└── TECHNICAL-ARCHITECTURE.md
```

---

## 🔌 External data providers

The provider layer is adapter-based so each source can expose a common contract, health status, provenance, and freshness state.

| Provider | Capability | Current role |
|---|---|---|
| [Open-Meteo](https://open-meteo.com/) | Current weather, forecast, ET₀, VPD, soil temperature/moisture | **Required** |
| [NASA POWER](https://power.larc.nasa.gov/) | 30-day historical agroclimate, precipitation, dry-spell and GDD calculations | **Required** |
| [Nominatim / OpenStreetMap](https://nominatim.openstreetmap.org/) | Forward and reverse geocoding | **Required** |
| [OpenAQ](https://openaq.org/) | PM₂.₅ / PM₁₀ and related environmental measurements | Optional |
| [Open Topo Data](https://www.opentopodata.org/) | Elevation from ETOPO1 | Optional |
| [GBIF](https://www.gbif.org/) | Regional species-occurrence observations | Optional |
| Agricultural news provider | Curated advisory/outbreak-style demo bulletins | Optional / demo |

### Provider cache

The in-process provider cache currently uses these TTLs:

| Data | TTL |
|---|---:|
| Weather | 30 min |
| Climate | 24 h |
| Geocoding | 7 days |
| Air quality | 1 h |
| Elevation | 7 days |
| Biodiversity | 24 h |
| News | 30 min |

Cached values can be served as stale data within the configured stale window, and concurrent requests for the same key are coalesced.

---

## 🤖 ML, RAG & AI status

### Crop disease

The current implementation is deliberately a **demo**:

- Architecture: PyTorch MobileNetV2 with three class slots.
- No trained weights are loaded by the active inference implementation.
- Image validity is checked with Pillow.
- The current inference path returns a deterministic `Leaf Blight` result with a fixed demo confidence value.
- The API marks the result as demo output and includes a limitation message.
- It is **not** a real field diagnosis.

See [models/disease/README.md](models/disease/README.md).

### Soil health

The current implementation is also a **prototype/synthetic model**:

- Model: XGBoost classifier.
- Features: nitrogen, phosphorus, potassium, pH, and moisture.
- The training script generates 1,000 synthetic samples using heuristic class rules.
- Classes: `Optimal`, `High Risk (pH imbalance)`, and `Suboptimal (Stress)`.
- The trained artifact is not committed to Git; running the training script creates `models/soil/soil_model_synthetic.pkl`.
- When that artifact is missing, the inference layer currently uses a deterministic demo fallback.

See [models/soil/README.md](models/soil/README.md).

### RAG

The advisory layer uses:

- [ChromaDB](https://www.trychroma.com/) persistent storage.
- `all-MiniLM-L6-v2` sentence-transformer embeddings.
- One chunk per Markdown document in the current demo corpus.
- Top-(k) retrieval before generation.
- A strict boundary: when no advisory evidence is retrieved, the service returns an insufficient-evidence response instead of inventing a recommendation.

The repository currently contains **three demo corpus documents**, not a field-curated agricultural knowledge base.

### LLM provider

Two providers are implemented:

1. **Local demo provider** — deterministic and available without credentials.
2. **IBM watsonx.ai / Granite** — used when `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` are configured.

The Granite path is configured through `ibm-watsonx-ai` and falls back to the local provider if the client cannot be initialized or a generation request fails.

---

## 🌦️ Risk engine

The risk engine is intentionally qualitative rather than a calibrated statistical model.

It currently derives:

- **Fungal pressure** from relative humidity, ambient temperature, precipitation, and upper-soil moisture.
- **Water stress** from dry-spell duration, recent rainfall, and ET₀.
- **Heat stress** from ambient temperature and vapour-pressure deficit.
- **Overall level** from those component signals.

The output exposes both a qualitative level and the underlying score/reason strings. These values are decision-support signals, not probabilities or agronomic guarantees.

---

## 🚀 Quick start

### Option 1 — Docker Compose

Prerequisites:

- Docker
- Docker Compose

Clone the repository:

```bash
git clone https://github.com/tejaswin-amara/AgriGuard-AI.git
cd AgriGuard-AI
cp .env.example .env
```

Start the services:

```bash
docker compose up --build -d
```

Services exposed by Compose:

| Service | URL | Purpose |
|---|---|---|
| Frontend | http://localhost | React static build served by Nginx |
| FastAPI Swagger | http://localhost:8000/docs | Interactive API documentation |
| FastAPI OpenAPI | http://localhost:8000/api/v1/openapi.json | OpenAPI schema |
| MinIO API | http://localhost:9000 | Object-storage API |
| MinIO Console | http://localhost:9001 | Object-storage console |
| PostgreSQL | localhost:5432 | Application database |

### Seed the demo RAG corpus

The ChromaDB vector store is generated at runtime and is not committed to Git.

From the repository root:

```bash
python rag/ingestion/ingest.py
```

Or, after the backend container is running:

```bash
docker compose exec backend python /app/rag/ingestion/ingest.py
```

### Generate the synthetic soil model

From the repository root:

```bash
python models/soil/train.py
```

This creates the local model artifact:

```text
models/soil/soil_model_synthetic.pkl
```

The artifact is intentionally kept out of Git.

---

## 🧪 Development & testing

### Backend

Create an environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r backend/requirements.txt
```

Run backend checks:

```cd backend
ruff check .
ruff format --check .
DATABASE_URL=sqlite:///./test.db PYTHONPATH=. pytest tests/ -v
```

Run the API locally:

```bash
cd backend
DATABASE_URL=postgresql://agriguard:agriguard@localhost:5432/agriguard \
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

npm run lint
npm run build
npx playwright install --with-deps chromium
npx playwright test
```

The frontend E2E configuration runs the production build through Vite preview on port 4173.

### Pre-commit

The repository includes hooks for:

- Gitleaks
- Ruff
- Ruff formatting
- standard pre-commit hygiene checks
- Biome formatting

Install and enable them with:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

---

## 📡 REST API

All application endpoints use the `/api/v1` prefix.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Application and required-provider health |
| POST | `/farms` | Create a farm |
| GET | `/farms` | List farms |
| GET | `/farms/{farm_id}` | Get a farm |
| GET | `/farms/{farm_id}/context` | Retrieve aggregated farm context |
| POST | `/location/geocode` | Forward geocode a location |
| GET | `/location/reverse` | Reverse geocode coordinates |
| GET | `/weather` | Current weather and forecast |
| GET | `/climate` | Historical climate summary |
| GET | `/environment/air-quality` | Air-quality data |
| GET | `/environment/elevation` | Elevation data |
| GET | `/biodiversity` | Regional biodiversity observations |
| GET | `/news` | Curated agricultural news/advisory data |
| GET | `/providers` | Registered provider status |
| GET | `/providers/health` | Provider health diagnostics |
| POST | `/disease/analyze` | Analyze a leaf image |
| POST | `/soil/advise` | Analyze soil inputs |
| POST | `/advisory/generate` | Generate a grounded advisory |
| GET | `/advisories` | List advisory history |
| GET | `/advisories/{id}` | Retrieve an advisory |

Interactive API documentation is available at http://localhost:8000/docs when the backend is running.

---

## 🔐 Data, provenance & responsible AI

AgriGuard AI is designed to make the difference between source data, model output, and generated text visible.

The API models explicitly represent:

- **Provenance** — provider, source URL, attribution, observed/retrieved timestamps, data quality, and freshness.
- **Data quality** — including weather-model, historical-climate, sensor, remote-sensing, ML-prediction, news-source, and heuristic categories.
- **Limitations** — model and advisory responses carry limitation text.
- **Risk context** — qualitative signals and explanations are returned alongside the main result.

The project deliberately avoids presenting its prototype outputs as field-validated certainty. Agricultural decisions, especially treatment and fertilizer decisions, should be verified with appropriate local agronomic expertise.

---

## ⚠️ Current limitations

The following points are part of the **current repository implementation** and are intentionally documented here rather than hidden behind “production-ready” language:

1. **Disease inference is a demo.** No trained disease weights are loaded by the active inference path.
2. **The soil model is synthetic.** Its training labels come from heuristic rules, not field measurements.
3. **The soil model artifact is generated locally.** A fresh clone does not contain `soil_model_synthetic.pkl`.
4. **The RAG corpus is a demo corpus.** It contains three local Markdown documents and is not a verified national agricultural advisory database.
5. **Agricultural news is currently a curated static provider.** It is not a live news aggregation service.
6. **Some provider failures have deterministic fallback behavior.** These fallbacks are for prototype resilience/testing and should not be interpreted as observations.
7. **MinIO is provisioned but not fully wired into the current disease upload flow.** The API records an image path, while the submitted bytes are handled in-memory by the request path.
8. **Alembic files exist, but application startup currently creates SQLModel tables directly.** Migrations are not the only database-initialization mechanism in the active code.
9. **The frontend uses a relative `/api/v1` API base URL.** The repository does not currently include a Vite API proxy or an Nginx reverse-proxy configuration for forwarding those requests to port 8000, so the Dockerized frontend/backend split may require additional routing configuration for full end-to-end browser use.
10. **There is no authentication layer in the current API.**

These limitations are important when evaluating the repository as a prototype versus a production system.

---

## 📚 Documentation

| Document | Purpose |
|---|---|
| [Demo Guide](docs/demo/DEMO.md) | Step-by-step evaluator flows |
| [Technical Architecture](TECHNICAL-ARCHITECTURE.md) | Architecture decisions and build-plan context |
| [Data & Models](DATA_AND_MODELS.md) | Handling of datasets and model artifacts |
| [Internship Compliance](docs/INTERNSHIP-COMPLIANCE.md) | 1M1B/AI-for-Sustainability compliance notes |
| [Security](SECURITY.md) | Security reporting and guidance |
| [Contributing](CONTRIBUTING.md) | Contribution workflow |
| [Changelog](CHANGELOG.md) | Repository change history |
| [Disease Model Notes](models/disease/README.md) | Disease-model limitations |
| [Soil Model Notes](models/soil/README.md) | Soil-model limitations |

---

## 🛠️ Technology stack

**Frontend**
React 19 · TypeScript 6 · Vite 8 · React Router 7 · Axios · Tailwind CSS · Biome · Playwright

**Backend**
Python 3.12 · FastAPI · Uvicorn · SQLModel · PostgreSQL · Pydantic Settings · Alembic

**Machine learning**
PyTorch · TorchVision · XGBoost · scikit-learn · NumPy

**RAG / AI**
ChromaDB · Sentence Transformers · IBM watsonx.ai / Granite · local deterministic demo provider

**Infrastructure / security**
Docker Compose · PostgreSQL · MinIO · GitHub Actions · Ruff · Biome · Gitleaks · Trivy · OpenTelemetry packages · Prometheus client

---

## 📜 License

AgriGuard AI is released under the [MIT License](LICENSE).

---

<div align="center">

**AgriGuard AI**

Context-aware agricultural intelligence, built as a transparent prototype.

</div>
