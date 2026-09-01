# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/), commit history follows [Conventional Commits](https://www.conventionalcommits.org/).

## [Unreleased]

### Added
- Project scoping: problem statement, SDG alignment (2, 13, 15), target users
- Full architecture and tool-stack decisions (`docs/TECHNICAL-ARCHITECTURE.md`)
- 1M1B internship submission deck
- Responsible AI principles (fairness, transparency, ethics, privacy)
- Repository documentation: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, this changelog
- Project-scoped `CLAUDE.md` for agent-assisted development
- Backend scaffold: FastAPI app, SQLModel schema, health check + 3 stub routes (disease/soil/advisory, all honest 501s), 4 passing tests
- Dev environment: `docker-compose.yml` (Postgres + MinIO + backend), `.env.example`, `.gitignore`
- CI workflow: automated tests + gitleaks secret scanning on every push/PR
- `.pre-commit-config.yaml`: gitleaks, ruff lint/format, basic file hygiene
- `docs/DATA_AND_MODELS.md`: model/dataset versioning strategy (a gap neither reference doc covered)
- `models/README.md`, `frontend/README.md`: scope and status for the two unstarted pieces
- `AGENTS.md`: canonical, tool-agnostic agent context — the file IBM Bob's `/init` reads and generates. `CLAUDE.md` slimmed to a pointer at it, avoiding two files that drift apart.
- **Corrected the LLM/RAG provider**: Anthropic's SDK → IBM watsonx.ai + Granite (`ibm-watsonx-ai`, verified installable). The 1M1B guideline document names IBM Granite Models as an allowed component directly; this is an IBM SkillsBuild-partnered internship. Updated across `docs/TECHNICAL-ARCHITECTURE.md`, `backend/app/core/config.py`, `backend/requirements.txt`, `.env.example`, and the advisory route's stub comments.

### Planned
- Frontend scaffold
- Disease detection model (CNN, transfer learning) — needs a real dataset first
- Soil health model (XGBoost) — needs a real dataset first
- RAG advisory layer — needs the ICAR / state advisory corpus assembled first
