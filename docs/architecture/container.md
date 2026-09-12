# Container
This document defines the high-level container architecture for AgriGuard AI.

## Containers
- **Frontend App**: React (Vite). Presents the interface.
- **Backend API**: FastAPI (Python). Provides orchestration.
- **Disease Model**: PyTorch CNN (MobileNetV2, Prototype).
- **Soil Model**: XGBoost (Synthetic tabular data).
- **RAG Component**: ChromaDB + SentenceTransformers.
- **LLM Component**: IBM Granite / Local Demo.
