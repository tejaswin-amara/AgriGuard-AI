# Project Alignment Matrix — 1M1B / AI-for-Sustainability Context

> **Important:** This is a repository self-assessment, not an official certification or statement of the program's current rules. Independent web verification of the program requirements was not available while this document was reconciled on 2026-09-30.

## Repository evidence

| Area | Current repository evidence | Assessment |
|---|---|---|
| Sustainability problem | Agricultural crop/soil decision support is the stated project domain | Implemented project framing |
| AI component | PyTorch MobileNetV2 demo architecture, XGBoost soil model, ChromaDB + sentence-transformers retrieval, optional IBM Granite generation | Implemented |
| End-to-end prototype | React frontend, FastAPI API, persistence, ML paths, RAG, and Docker Compose are present | Implemented, with deployment caveats |
| Responsible AI | Provenance, freshness, limitation fields, qualitative risk signals, and explicit demo/synthetic labeling | Implemented in code/UI |
| Transparency | Results expose limitation/model-provenance information and RAG citations | Implemented |
| Privacy | Application minimizes explicit user fields, but farm coordinates are currently stored because they are part of the location/context flow | Partial; production privacy controls are not implemented |
| Dataset realism | Disease inference is deterministic demo logic; soil training data is synthetic | Prototype only |
| Knowledge grounding | Three local Markdown demo documents are retrieved through ChromaDB | Implemented as demo functionality |
| Production readiness | No authentication, rate limiting, hardened secrets integration, or production deployment configuration | Not implemented |
| Verification | Latest inspected main CI run has backend/security/Docker success but frontend Biome failure | Not currently all-green |

## Current prototype boundaries

The repository should be presented as a working technical prototype. Its ML outputs and demo advisory corpus are not evidence of field performance.

The project should not claim:

- field-validated crop-disease accuracy;
- laboratory-validated soil classification;
- production-grade agronomic prescriptions;
- production authentication or privacy guarantees;
- an all-green CI pipeline until a later workflow run proves it.

## Related evidence

- [README](../README.md)
- [Dataset Card](dataset-card/DATASET_CARD.md)
- [Disease Model Card](model-card/DISEASE_MODEL_CARD.md)
- [Soil Model Card](model-card/SOIL_MODEL_CARD.md)
- [Responsible AI page](https://github.com/tejaswin-amara/AgriGuard-AI/blob/main/frontend/src/pages/ResponsibleAI.tsx)
