# Runbook — External Provider Outages & Degradation

## Overview

AgriGuard AI integrates several external provider adapters. A provider may fail independently without necessarily making the entire farm-context request fail.

## Provider classes

| Provider | Required flag | Capability |
|---|---|---|
| Open-Meteo | Required | Weather |
| NASA POWER | Required | Historical climate |
| Nominatim | Required | Geocoding |
| OpenAQ | Optional | Air quality |
| Open Topo Data | Optional | Elevation |
| GBIF | Optional | Biodiversity |
| Curated agriculture news | Optional | Demo news/advisory |

## Automatic behavior

### Cache

The provider cache can return cached or stale values according to capability-specific TTLs.

### Farm context

Farm-context provider calls use concurrent execution with exception isolation. Optional failures become missing context rather than terminating the whole aggregation.

### Prototype fallbacks

Current source code contains deterministic fallbacks for:

- weather;
- climate;
- OpenAQ air-quality values;
- farm creation when geocoding fails.

These values are synthetic. They must be labeled or removed before any production deployment.

## Diagnostics

```http
GET /api/v1/providers/health
GET /api/v1/health
```

## Recovery

1. Confirm the upstream service is reachable.
2. Inspect the provider error message and freshness state.
3. Verify whether cached data exists.
4. Restore the upstream dependency or update the adapter.
5. Re-run the corresponding provider and API tests.

