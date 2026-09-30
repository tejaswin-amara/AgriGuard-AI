# ADR 0001 — Capability-Based External Provider Architecture

- **Status:** Accepted
- **Date:** 2026-09-26
- **Scope:** External data integrations in `backend/app/services/external/`

## Context

AgriGuard AI needs location, weather, historical climate, air quality, elevation, biodiversity, and agricultural-news inputs without coupling application services to individual third-party response formats.

## Decision

Use capability-specific provider interfaces derived from `ExternalDataProvider`:

- `WeatherProvider`
- `ClimateProvider`
- `GeocodingProvider`
- `AirQualityProvider`
- `ElevationProvider`
- `BiodiversityProvider`
- `NewsProvider`

Concrete providers translate third-party responses into the repository's typed Pydantic models and attach `Provenance` metadata.

A central `ProviderRegistry` exposes provider health information. A small in-process `ProviderCache` handles TTLs, freshness states, stale-cache serving, and in-flight request coalescing.

## Current providers

| Capability | Implementation | Required |
|---|---|---|
| Weather | Open-Meteo | Yes |
| Climate | NASA POWER | Yes |
| Geocoding | Nominatim / OpenStreetMap | Yes |
| Air quality | OpenAQ | No |
| Elevation | Open Topo Data / ETOPO1 | No |
| Biodiversity | GBIF | No |
| News | Curated agriculture demo provider | No |

Mock providers also exist under `mock_providers.py` for tests/prototype scenarios.

## Consequences

### Positive

- Third-party API formats remain outside core business logic.
- Providers are replaceable behind stable contracts.
- Health, provenance, and freshness are represented consistently.
- Optional provider failures can be isolated from core farm-context assembly.

### Trade-offs and known limitations

- Provider availability is external to the application.
- The current farm-context service still uses deterministic weather/climate mock fallbacks when live calls fail.
- The current OpenAQ adapter also contains deterministic fallback values on failure.
- The current farm-creation route contains a hard-coded geocoding fallback; this is prototype behavior and should be removed before production use.
- In-process caching is not shared between multiple backend instances.
