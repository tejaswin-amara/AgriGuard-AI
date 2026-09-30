# Changelog

All notable changes to this project are documented here. Commit messages follow Conventional Commits.

## [Unreleased] — Documentation Reconciliation — 2026-09-30

### Changed

- Rebuilt the repository README around the current implementation.
- Reconciled the technical architecture with the code currently present on `main`.
- Updated dataset and model cards to distinguish demo/synthetic behavior from field-validated ML.
- Documented the actual disease inference path and its deterministic demo output.
- Documented the current synthetic XGBoost soil pipeline and generated artifact.
- Updated architecture ADRs, context, data-flow, deployment, and threat-model documentation.
- Rebuilt the demo guide and all operational runbooks.
- Updated security documentation to reflect stored farm coordinates and the absence of authentication/rate limiting.
- Updated agent documentation so `AGENTS.md` is a current-state source rather than a planned-state summary.
- Updated the frontend README to remove the unused Vite starter template and describe the actual application.
- Updated the completion report to reflect the latest inspected CI state.
- Separated historical hardening claims from current implementation behavior where the current source and historical notes differ.

### Current verification note

The latest inspected `main` CI run on 2026-09-29 had successful backend, security, and Docker jobs, while the frontend job failed at the Biome step with 29 reported errors. Frontend build and Playwright were skipped for that run.

## [2.0.0] - 2026-09-26 — Production Hardening & Repository Fixes

This section is preserved as historical project history. Its listed changes describe work recorded at the time; for current behavior, prefer the implementation and the current-state documents above.

### Fixed

- Advisory history API contract changes were recorded.
- Geocoding, external-provider, RAG, CORS, ML-confidence, frontend-type, and import-cleanup hardening work was recorded.
- Database migration scaffolding and integration/E2E testing were recorded.

### Added

- Alembic migration framework.
- Database integration tests.
- Expanded Playwright journeys.
- RAG grounding and security tests.

## [1.0.0] — Initial Prototype

### Added

- Initial 1M1B project scoping and architecture documentation.
- FastAPI backend scaffold.
- SQLModel data layer.
- React/Vite frontend.
- Initial ML/RAG prototype.
- Docker Compose development environment.
