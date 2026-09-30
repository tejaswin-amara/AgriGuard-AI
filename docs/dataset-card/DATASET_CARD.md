# Dataset Card — AgriGuard AI Prototype

> **Status:** Demo / synthetic inputs. This is not a production dataset card.

## 1. What data exists today?

The current repository does **not** contain a field-validated crop-disease training dataset or a field-measured soil-health training dataset.

The system currently uses three distinct data categories:

| Data category | Current contents | Used by |
|---|---|---|
| Disease model data | No trained dataset is loaded by the active inference path | Disease demo |
| Soil model data | 1,000 synthetic rows generated from heuristic rules by `models/soil/train.py` | XGBoost soil model |
| Advisory knowledge | Three local Markdown demo documents in `rag/corpus/` | ChromaDB RAG |

## 2. Disease model data

The disease directory contains a MobileNetV2 architecture definition and deterministic inference code. The active inference path validates an uploaded image but does not run trained weights.

The service-level provenance text mentions the PlantVillage public leaf dataset, but the current repository does not ship a PlantVillage-derived training pipeline or trained checkpoint. That provenance string should therefore not be interpreted as evidence that the deployed demo was trained or evaluated on PlantVillage.

## 3. Soil model data

The soil training script generates 1,000 synthetic samples using:

- Nitrogen: 10–150
- Phosphorus: 5–80
- Potassium: 10–100
- pH: 4.5–8.5
- Moisture: 10–60

Class labels are generated from heuristic thresholds. They are not laboratory labels and do not represent validated agronomic ground truth.

## 4. Advisory corpus

The current corpus contains three Markdown documents:

- Leaf blight management
- Soil pH management
- Moisture stress mitigation

Each document has simple front matter with title, organization, date, and identifier metadata. The ingestion script currently stores one chunk per document.

The corpus is a demonstration knowledge base. It should not be described as a verified ICAR, state-department, or national agricultural evidence base.

## 5. Data governance assumptions

The prototype intentionally avoids unnecessary personal information. Farm records currently store a location query plus resolved latitude/longitude and crop information because those values are required for the context pipeline.

The repository does not implement a consent-management workflow, retention policy, or production privacy controls yet.

## 6. Dataset risks

The current data has major limitations:

- no field validation for disease inference;
- no real-world soil labels;
- synthetic class boundaries;
- very small RAG corpus;
- no demonstrated geographic or crop coverage;
- no measured model generalization;
- no independently verified clinical/agronomic outcome data.

## 7. Before production use

A production dataset program would need:

1. documented source licenses and provenance;
2. representative crop, disease, soil, region, and season coverage;
3. train/validation/test separation;
4. leakage checks;
5. class-balance analysis;
6. field/lab validation;
7. versioned dataset manifests;
8. reproducible model-training records;
9. dataset and model bias assessment.

