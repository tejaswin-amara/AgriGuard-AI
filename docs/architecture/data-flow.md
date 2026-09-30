# Data Flow

## 1. Farm context

```text
Farm setup
  -> Nominatim geocoding
  -> Farm record
  -> FarmContextService
      -> Open-Meteo
      -> NASA POWER
      -> OpenAQ
      -> Open Topo Data
      -> GBIF
      -> curated news provider
  -> RiskEngine
  -> FarmContextResponse
  -> React dashboard
```

Provider calls are made concurrently and decorated with freshness/provenance information.

## 2. Disease analysis

```text
Leaf image
  -> MIME + 10 MB validation
  -> deterministic MobileNetV2 demo inference contract
  -> DiseaseAnalysis persistence
  -> RAG retrieval for disease-management context
  -> optional LLM generation
  -> API response
```

The current disease inference path does not load trained weights.

## 3. Soil analysis

```text
N / P / K / pH / moisture
  -> Pydantic validation
  -> XGBoost synthetic-data model (when artifact exists)
  -> SoilReading persistence
  -> RAG retrieval
  -> optional LLM generation
  -> API response
```

The model was trained from synthetic heuristic labels.

## 4. Advisory generation

```text
Disease/soil/general query
  -> ChromaDB similarity retrieval
  -> retrieved advisory passages
  -> grounding prompt
  -> local demo provider OR IBM Granite
  -> AdvisoryRecord persistence
  -> cited advisory response
```

When no evidence is retrieved, the advisory service returns an insufficient-evidence response rather than generating unsupported advice.
