# 1. External Provider Capability-Based Architecture

* Status: Accepted
* Date: 2026-09-26

## Context

AgriGuard AI requires live weather, historical climate baseline, geocoding, air quality, terrain elevation, biodiversity, and outbreak news integration to produce context-aware agricultural advisories.

## Decision

We designed a capability-based adapter pattern (`WeatherProvider`, `ClimateProvider`, `GeocodingProvider`, `AirQualityProvider`, `ElevationProvider`, `BiodiversityProvider`, `NewsProvider`) extending an abstract `ExternalDataProvider`.

All external API interactions are encapsulated inside provider adapters. They return strongly typed domain models (`WeatherData`, `ClimateData`, `GeocodedLocation`) with explicit `Provenance` tracking.

## Consequences

* **Decoupling**: The core application logic and React frontend never interact with raw third-party JSON payloads.
* **Replaceability**: A provider (e.g. Open-Meteo) can be swapped or augmented without altering frontend components or FastAPI route contracts.
* **Resilience**: Optional providers (OpenAQ, Open Topo Data, GBIF) fail gracefully without disrupting core disease or soil advisory workflows.
