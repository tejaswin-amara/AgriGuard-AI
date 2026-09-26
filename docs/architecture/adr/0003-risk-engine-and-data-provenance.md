# 3. Risk Engine Semantics & Data Provenance Framework

* Status: Accepted
* Date: 2026-09-26

## Context

Combining ML predictions with external meteorological parameters risks manufacturing false statistical probabilities if heuristic rules are conflated with validated probabilistic models.

## Decision

We built `RiskEngine` (`backend/app/services/risk_engine.py`) to generate qualitative pressure levels (`low`, `moderate`, `elevated`, `severe`) and meteorological explanations (e.g., high relative humidity + recent rainfall) without outputting uncalibrated probability numbers.

Furthermore, every response carries explicit `Provenance` metadata distinguishing data quality (`WEATHER_MODEL`, `HISTORICAL_CLIMATE`, `SENSOR_MEASUREMENT`, `ML_PREDICTION`, `LLM_OUTPUT`, `NEWS_SOURCE`) and freshness state (`FRESH`, `CACHED`, `STALE`, `UNAVAILABLE`).

## Consequences

* **Responsible AI Alignment**: Prevents misleading farmers with artificial certainty.
* **Explainability**: Clear meteorological drivers accompany every risk level.
* **Auditability**: Generated advisories record complete context, model versions, and source citations in the database.
