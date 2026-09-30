# Data & Model Artifacts

> **Current-state reference:** 2026-09-30

This repository keeps model code and reproducible generation logic in Git while treating generated ML artifacts and derived vector stores as rebuildable state.

## What is committed

### Model code

Committed:

- `models/disease/model.py`
- `models/disease/inference.py`
- `models/soil/train.py`
- `models/soil/inference.py`

### RAG code and corpus

Committed:

- `rag/corpus/*.md`
- `rag/ingestion/ingest.py`
- `rag/retrieval/retrieve.py`

The current corpus contains three Markdown demo documents.

## What is generated locally

### Soil model artifact

Running:

```bash
python models/soil/train.py
```

generates:

```text
models/soil/soil_model_synthetic.pkl
```

The artifact is excluded from version control.

### ChromaDB vector store

Running:

```bash
python rag/ingestion/ingest.py
```

creates a persistent ChromaDB store under:

```text
rag/vector_db/
```

This is derived from the Markdown corpus and should be rebuildable.

## Disease model status

The current disease inference path does not require a trained model artifact. The MobileNetV2 architecture exists as a structural definition, while the active inference implementation returns deterministic demo output.

## Data provenance

The repository does not currently contain a field-validated disease dataset or laboratory soil dataset.

The soil labels are generated from heuristic rules over synthetic data.

A service-level disease provenance field mentions PlantVillage, but the active inference path does not load a PlantVillage-trained checkpoint.

## Versioning policy

Do not commit large generated weights or vector stores merely to make a demo work. Keep:

- training/inference code in Git;
- corpus source documents in Git when small enough and legally appropriate;
- generated model artifacts outside Git;
- generated ChromaDB state outside Git.

For a real training program, add a dedicated data/model versioning workflow only when the dataset and artifact lifecycle actually requires it.
