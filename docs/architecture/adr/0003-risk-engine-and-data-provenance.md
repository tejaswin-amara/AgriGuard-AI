# ADR 0003 — Qualitative Risk Signals and Explicit Provenance

- **Status:** Accepted
- **Date:** 2026-09-26
- **Implementation:** `backend/app/services/risk_engine.py`

## Context

Combining model outputs and environmental values can create a misleading impression of statistical certainty. The prototype needs a clear distinction between measurements/models, heuristics, generated text, and data freshness.

## Decision

The risk engine emits qualitative signals, not calibrated probabilities.

Current signal domains:

| Signal | Current levels |
|---|---|
| Fungal pressure | `low`, `moderate`, `elevated` |
| Water stress | `optimal`, `moderate`, `severe` |
| Heat stress | `none`, `mild`, `high` |
| Overall | `low`, `moderate`, `elevated` |

Rules consider available humidity, temperature, precipitation, soil moisture, dry-spell duration, rainfall totals, ET₀, VPD, and climate context.

External and generated data models carry provenance fields including provider identity, source URL where available, timestamps, data-quality class, freshness state, and attribution.

## Consequences

- Risk output is explicitly heuristic rather than a probability estimate.
- Explanations expose the environmental drivers used by the current rules.
- Freshness and provenance can be rendered by the frontend.
- The implementation can still be wrong or incomplete; provenance does not establish correctness.
- Thresholds are domain heuristics and have not been calibrated against field outcomes.
