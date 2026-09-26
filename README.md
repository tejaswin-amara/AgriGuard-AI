# AgriGuard AI — Context-Aware Agricultural Intelligence Platform

[![Backend Test Suite](https://github.com/tejaswin-amara/AgriGuard-AI/actions/workflows/backend.yml/badge.svg)](https://github.com/tejaswin-amara/AgriGuard-AI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![React 19](https://img.shields.io/badge/React-19.0-sky.svg)](https://react.dev/)

AgriGuard AI is a context-aware agricultural decision-support platform designed for smallholder farmers. It combines crop leaf disease computer vision, soil health classification, live weather metrics, 30-day historical agroclimate baselines, environmental air quality, terrain relief, biodiversity observations, and outbreak news with Retrieval-Augmented Generation (RAG) and IBM WatsonX Granite model reasoning.

---

## Integrated Public API Catalog Matrix

| Provider | Capability | Priority | Auth | Cache Policy | Attribution / Source |
|---|---|---|---|---|---|
| Open-Meteo | Live weather, forecast, ET0, VPD, soil temp/moisture | Core (Required) | None | 30 minutes | Open-Meteo.com |
| NASA POWER | 30-day historical agroclimate, rain, GDD | Core (Required) | None | 24 hours | NASA POWER Agroclimate Program |
| Nominatim OSM | Forward & Reverse Geocoding | Core (Required) | None (User-Agent) | 7 days | OpenStreetMap Contributors |
| OpenAQ | Environmental Air Quality (PM2.5, PM10) | Optional | None | 1 hour | OpenAQ Community |
| Open Topo Data | Terrain Elevation & Relief | Optional | None | 7 days | ETOPO1 Global Relief Model |
| GBIF | Regional Biodiversity & Species Occurrences | Optional | None | 24 hours | Global Biodiversity Information Facility |
| Agri News | Outbreak & Extension News Bulletins | Optional | None | 30 minutes | Curated Agricultural Extension Feeds |

---

## Getting Started

### Prerequisites

* Python 3.12+
* Node.js 22+ & npm
* Docker & Docker Compose (Optional)

### Local Development Setup

1. Clone the repository:
   git clone https://github.com/tejaswin-amara/AgriGuard-AI.git
   cd AgriGuard-AI

2. Backend Setup:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   PYTHONPATH=backend pytest
   PYTHONPATH=backend uvicorn app.main:app --reload --port 8000

3. Frontend Setup:
   cd frontend
   npm ci
   npm run lint
   npm run build

### Running with Docker Compose

docker compose up --build -d

Access the application at:
* Frontend UI: http://localhost/
* FastAPI Backend Swagger Docs: http://localhost:8000/docs
* MinIO Console: http://localhost:9001/

---

## REST API Surface Summary

* GET /api/v1/health — System and provider health status
* POST /api/v1/farms — Create and geocode a farm plot
* GET /api/v1/farms/{farm_id}/context — Retrieve aggregated farm context
* POST /api/v1/disease/analyze — Leaf image disease CNN classification
* POST /api/v1/soil/advise — NPK & pH soil health classification
* POST /api/v1/advisory/generate — Generate grounded RAG advisory
* GET /api/v1/advisories — List historical advisory audit trail
* GET /api/v1/providers/health — Provider capability health diagnostics

---

## Responsible AI & Governance

1. Zero Hallucination Grounding: Advisory recommendations are strictly grounded in retrieved extension documents.
2. Explicit Provenance: Data points carry provenance badges distinguishing OBSERVED, WEATHER_MODEL, HISTORICAL_CLIMATE, ML_PREDICTION, and SYNTHETIC origins.
3. Qualitative Risk Signals: Risk engine outputs qualitative pressure levels (low, moderate, elevated, severe) with plain-language meteorological explanations.
