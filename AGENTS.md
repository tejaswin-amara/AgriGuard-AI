# AGENTS.md — AgriGuard AI

> **Canonical agent context.** Keep this file synchronized with the actual repository. Do not describe planned architecture as implemented behavior.

## Project

AgriGuard AI is a full-stack agricultural decision-support prototype focused on farm context, soil analysis, crop-disease demonstration, environmental signals, and grounded advisory generation.

Primary repository: `tejaswin-amara/AgriGuard-AI`

## Current implementation

### Frontend

- React 19
- TypeScript
- Vite
- React Router
- Axios
- Tailwind CSS
- i18next / react-i18next
- Biome
- Playwright

### Backend

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic / pydantic-settings
- SQLModel
- PostgreSQL
- Alembic configuration and initial revision

### ML / RAG

- PyTorch / TorchVision MobileNetV2 structural disease model
- deterministic disease demo inference
- XGBoost synthetic soil classifier
- ChromaDB
- sentence-transformers `all-MiniLM-L6-v2`
- IBM watsonx.ai / Granite optional provider
- deterministic local advisory provider

### Infrastructure

- Docker Compose
- PostgreSQL 16
- MinIO
- GitHub Actions
- Gitleaks
- Trivy
- Dependabot

## Current truth about prototype status

Do not call the project production-ready.

- Disease inference does not load trained weights.
- Disease output is deterministic demo behavior.
- Soil labels come from synthetic heuristic data.
- The RAG corpus contains three demo documents.
- Agricultural news is a curated static provider.
- Provider fallbacks can return deterministic synthetic values.
- MinIO is provisioned, but the current disease path does not persist the uploaded bytes through MinIO.
- Authentication/authorization is absent.
- The frontend uses relative `/api/v1` requests while the shipped frontend Nginx container has no backend reverse-proxy rule.
- Alembic exists, but current application startup calls SQLModel metadata table creation.
- The latest inspected CI run has a frontend Biome failure.

## Engineering rules

1. Never present synthetic or fallback values as observations.
2. Never present deterministic demo model outputs as validated predictions.
3. Never claim a probability is calibrated without measurement.
4. Never make an advisory recommendation without retrieved evidence.
5. Keep provenance, freshness, and limitations visible.
6. Minimize farmer data collection.
7. Prefer plain-language advisory copy.
8. Update documentation whenever code behavior changes.
9. Prove verification claims with an actual test/check.
10. Never commit secrets or generated large ML/vector artifacts.

## Key documentation

- `README.md`
- `TECHNICAL-ARCHITECTURE.md`
- `DATA_AND_MODELS.md`
- `docs/dataset-card/`
- `docs/model-card/`
- `docs/architecture/`
- `docs/runbooks/`
- `docs/demo/DEMO.md`
- `SECURITY.md`
- `CHANGELOG.md`
