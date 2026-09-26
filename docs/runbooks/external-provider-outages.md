# Operational Runbook: External Provider Outages & Degradation

## Overview

AgriGuard AI integrates multiple public API providers (Open-Meteo, NASA POWER, Nominatim, OpenAQ, Open Topo Data, GBIF). This runbook outlines diagnostic steps and operational recovery when external providers experience degradation or downtime.

## Automatic Resilience Behavior

1. **Required Core Providers (Open-Meteo, NASA POWER, Nominatim)**:
   - Shared transport retries transient errors (5xx, 429) up to 2 times with exponential backoff.
   - If live calls fail, `ProviderCache` serves stale cached data up to 4x TTL labeled as `STALE`.
   - If no cached data exists, deterministic mock fallbacks fill required structure to prevent application crash.

2. **Optional Providers (OpenAQ, Open Topo Data, GBIF, News)**:
   - Executed with `return_exceptions=True`.
   - Outages set status to `UNAVAILABLE` without impacting disease classification or soil advisory.

## Health Diagnostics

Check provider statuses via REST API:

```http
GET /api/v1/providers/health
```

Sample Response:

```json
[
  {
    "provider_id": "open_meteo",
    "name": "Open-Meteo Weather API",
    "category": "weather",
    "status": "healthy",
    "latency_ms": 142.5
  }
]
```

## Manual Actions

If a provider endpoint is permanently retired or URL changes:
1. Update `base_url` in the specific adapter inside `backend/app/services/external/providers/`.
2. Re-run backend test suite: `PYTHONPATH=backend pytest`.
