# ADR 0002 — Centralized Farm Context Orchestration

- **Status:** Accepted
- **Date:** 2026-09-26
- **Implementation:** `backend/app/services/farm_context.py`

## Context

Dashboard and other user flows need a normalized view of the selected farm: location, weather, climate, environmental context, provider health, freshness, and risk signals.

Calling every external provider directly from individual route handlers would duplicate orchestration, error handling, cache access, and normalization logic.

## Decision

Use `FarmContextService` as the orchestration boundary.

The service:

1. Resolves or reverse-resolves the farm location.
2. Builds cache keys for each external capability.
3. Starts provider requests concurrently with `asyncio.gather`.
4. Collects failures without failing the whole aggregation.
5. Uses cached/stale values when available.
6. Uses deterministic mock weather/climate fallbacks in the current prototype when live values are unavailable.
7. Sends the resulting weather/climate/elevation inputs to `RiskEngine`.
8. Returns a single typed `FarmContextResponse`.

## Consequences

### Positive

- One normalized contract for frontend farm intelligence.
- Concurrent external requests reduce serial waiting.
- Request coalescing reduces duplicate calls within the process.
- Provider status and data freshness are available alongside values.

### Trade-offs

- A single aggregation request depends on several services.
- Partial data is possible and must remain visibly labeled.
- The current deterministic mock fallbacks can produce values that look realistic; callers must respect provenance/freshness and prototype limitations.
- In-process cache state disappears when the backend process restarts.
