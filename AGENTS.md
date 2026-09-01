# AGENTS.md — AgriGuard AI

Persistent project context for any AI coding agent working in this repo — IBM Bob, Claude Code, Codex, Cursor, or otherwise. This is the canonical file; agent-specific files (like `CLAUDE.md`) point here rather than duplicating it, so the two can't drift out of sync.

## What This Project Is

AI-powered crop disease and soil health advisory for smallholder Indian farmers, built for the 1M1B AI for Sustainability Virtual Internship (with IBM SkillsBuild and AICTE). Two models (image classifier + tabular soil-health model) feed a RAG-grounded advisory layer. Full reasoning: `docs/TECHNICAL-ARCHITECTURE.md`.

## Current Status

**Full Prototype Implemented and Tested** — FastAPI + SQLModel, React frontend, ML inference stubs and RAG. Verify it before trusting this file:

```bash
docker compose up --build
```
Or manually run the backend and frontend.

**Important**: The disease model is a PyTorch demo, the soil model is trained on synthetic data, and the RAG corpus uses demo documents. Don't reference a model prediction or corpus document as if it were field-tested.

## Tech Stack Defaults for This Repo

Full reasoning and every alternative considered: `docs/TECHNICAL-ARCHITECTURE.md`. The short version:

| Task | Choice | Why |
|---|---|---|
| Backend | `fastapi/full-stack-fastapi-template` conventions | Core workload is Python ML (CNN + XGBoost) |
| Data layer | SQLModel + PostgreSQL | Bundled with the FastAPI template |
| LLM / RAG provider | **IBM watsonx.ai + Granite models** (`ibm-watsonx-ai` SDK) | IBM SkillsBuild-partnered internship. Local demo fallback implemented. |
| Frontend | React + Vite | Clean UI building. |
| Object storage | MinIO | Stores submitted leaf images. |

## Non-Negotiables (Domain-Specific)

- **Never let the advisory layer state a recommendation that isn't grounded in a retrieved source passage.**
- **Never add a new farmer data field without a stated reason it needs to exist.** Default to collecting less.
- **Low-confidence or high-severity flags route to "consult an agronomist,"** not an auto-recommendation.
- **Keep advisory copy in plain language.**
