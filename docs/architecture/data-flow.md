# Data Flow
This document defines the high-level data flow architecture for AgriGuard AI.

## Workflow
1. User provides inputs (crop image / soil data) via Frontend.
2. Frontend sends request to Backend API.
3. Backend triggers ML classification models (Disease / Soil).
4. Results are passed to RAG Retriever.
5. RAG fetches relevant context.
6. Context + Classification -> LLM.
7. Advisory is sent back to User.
