# AGENTS.md — AgriGuard AI

Persistent project context for any AI coding agent working in this repo — IBM Bob, Claude Code, Codex, Cursor, or otherwise. This is the canonical file; agent-specific files (like `CLAUDE.md`) point here rather than duplicating it, so the two can't drift out of sync.

## What This Project Is

AI-powered crop disease and soil health advisory for smallholder Indian farmers, built for the 1M1B AI for Sustainability Virtual Internship (with IBM SkillsBuild and AICTE). Two models (image classifier + tabular soil-health model) feed a RAG-grounded advisory layer. Full reasoning: `docs/TECHNICAL-ARCHITECTURE.md`.

## Current Status

**Backend scaffold is real and tested** — FastAPI + SQLModel, health check working, 3 model-facing routes wired as honest 501 stubs, 4 passing tests (`backend/tests/`). Verify it before trusting this file:

```bash
cd backend && pip install -r requirements.txt
DATABASE_URL=sqlite:///./test.db python -m pytest tests/ -v
```

**Not yet real:** frontend (see `frontend/README.md`), any trained model, the RAG advisory corpus. Don't reference a model prediction, a frontend component, or a corpus document as if it exists — none of them do yet.

## Tech Stack Defaults for This Repo

Full reasoning and every alternative considered: `docs/TECHNICAL-ARCHITECTURE.md`. The short version:

| Task | Choice | Why |
|---|---|---|
| Backend | `fastapi/full-stack-fastapi-template` conventions | Core workload is Python ML (CNN + XGBoost) — not a TypeScript fit |
| Data layer | SQLModel + PostgreSQL | Bundled with the FastAPI template |
| LLM / RAG provider | **IBM watsonx.ai + Granite models** (`ibm-watsonx-ai` SDK) | This is an IBM SkillsBuild-partnered internship — its own guideline document lists IBM Granite Models as an allowed component. Using IBM's own stack here is the better contextual fit, not just a technical one. Any other provider is a valid fallback, not the default. |
| Language support | i18next / react-i18next | **Adopted, not situational** — most end users won't read English |
| Accessibility | axe-core | **Adopted, not situational** — low-end devices and screen-reader use are real for this audience |
| Object storage | MinIO | Stores submitted leaf images for audit/retraining |

## Non-Negotiables (Domain-Specific)

- **Never let the advisory layer state a recommendation that isn't grounded in a retrieved source passage.** If retrieval comes back empty or low-confidence, say so — don't fill the gap with the model's own unsupported claim.
- **Never add a new farmer data field without a stated reason it needs to exist.** Default to collecting less (see Privacy principle, `README.md`).
- **Low-confidence or high-severity disease flags route to "consult an agronomist,"** not a confident auto-recommendation.
- **Keep advisory copy in plain language.** No model jargon, no raw confidence scores on the farmer-facing side.

## Where to Look

| Need | File |
|---|---|
| Full tool-stack reasoning | `docs/TECHNICAL-ARCHITECTURE.md` |
| Model/dataset versioning strategy | `docs/DATA_AND_MODELS.md` |
| Contribution process | `CONTRIBUTING.md` |
| What's done vs. planned | `CHANGELOG.md`, `README.md` Roadmap |
| Responsible AI principles | `README.md` (Responsible AI section) |

## For IBM Bob Specifically

Bob's `/init` will likely want to regenerate or extend this file — that's expected and fine. If it does, keep the Non-Negotiables section intact; it encodes decisions from `docs/TECHNICAL-ARCHITECTURE.md` that shouldn't get silently dropped by an auto-generated rewrite. Bob's own MCP support (see IBM's docs at `bob.ibm.com/docs`) can wrap the FastAPI backend's endpoints as tools directly once they're real — the OpenAPI schema FastAPI generates at `/openapi.json` is a natural bridge for that.
