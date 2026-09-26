# 2. Centralized FarmContextService Orchestration

* Status: Accepted
* Date: 2026-09-26

## Context

Multiple application endpoints (Dashboard, Insights, Disease Analysis, Soil Advisory) require aggregated environmental and meteorological context per farm plot. Scattered API calls would lead to duplicate external requests, race conditions, and inconsistent context structures.

## Decision

We introduced `FarmContextService` (`backend/app/services/farm_context.py`) as the single central orchestration layer.

It resolves farm location, executes parallel asynchronous provider requests (`asyncio.gather`), applies request coalescing/deduplication, interacts with `RiskEngine`, and returns a single normalized `FarmContextResponse`.

## Consequences

* **Single Source of Truth**: All components receive an identical, strongly-typed `FarmContextResponse`.
* **Performance**: Independent provider calls execute concurrently rather than serially.
* **Request Deduplication**: In-flight request coalescing prevents duplicate external API hits when UI views render simultaneously.
