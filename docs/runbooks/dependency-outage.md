# Runbook — Dependency Outage

## Scope

External API or AI-provider outage affecting AgriGuard AI.

## Identify the failing dependency

Check:

```http
GET /api/v1/providers/health
```

Core external adapters:

- Open-Meteo
- NASA POWER
- Nominatim

Optional adapters:

- OpenAQ
- Open Topo Data
- GBIF
- curated agriculture news

## Current resilience behavior

The provider cache supports:

- per-capability TTLs;
- in-flight request coalescing;
- stale-cache serving within the configured stale window.

The farm-context service also contains deterministic weather/climate mock fallbacks. These are prototype resilience values and must never be presented as real observations.

The OpenAQ provider also contains deterministic fallback values on failure.

## IBM Granite outage

When the IBM watsonx.ai client is unavailable or generation fails, the LLM layer falls back to the local deterministic provider.

## Operator response

1. Confirm provider health.
2. Check whether the response is fresh, cached, stale, or unavailable.
3. Avoid treating synthetic fallback values as live observations.
4. If the provider is permanently changed, update its adapter and provider tests.
5. Re-run backend and frontend checks before deployment.
