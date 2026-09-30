# System Context

## Purpose

AgriGuard AI is a prototype agricultural decision-support application. It combines farm inputs with environmental context, model demonstrations, and retrieved advisory documents.

## Actors

### Primary user

- Smallholder or marginal farmer using the web interface.

### Supporting users / stakeholders

- Agricultural extension or advisory personnel.
- Project evaluators and developers.

The current application does not implement separate authenticated roles.

## External systems

- Open-Meteo — weather and forecast.
- NASA POWER — historical agroclimate.
- Nominatim / OpenStreetMap — geocoding.
- OpenAQ — air quality.
- Open Topo Data — elevation.
- GBIF — biodiversity observations.
- Curated agriculture news provider — demonstration news/advisory content.
- IBM watsonx.ai / Granite — optional generated advisory provider.

## Trust boundary

User-provided soil values and image uploads enter through FastAPI request validation. External responses are normalized into typed models before reaching application logic. Retrieved RAG text is passed as passive reference context to the LLM layer.
