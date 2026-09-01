# 1M1B Internship Compliance Matrix

This document maps the AgriGuard AI project to the official requirements of the "1M1B AI for Sustainability Virtual Internship".

| Requirement | Status | Evidence in Repository |
|-------------|--------|------------------------|
| **Real sustainability problem** | PASS | Addressed crop loss and soil degradation for smallholder farmers. Documented in `README.md` and frontend About page. |
| **Primary SDG** | PASS | SDG 2 (Zero Hunger) explicitly targeted in `README.md` and About page. |
| **Secondary SDGs** | PASS | SDG 13 (Climate Action) and 15 (Life on Land) targeted. |
| **Target users** | PASS | Smallholder and marginal farmers, extension officers. |
| **AI usage** | PASS | Uses PyTorch (CNN structure), XGBoost (tabular), and LLM/RAG (ChromaDB + sentence-transformers). |
| **Prototype/Demo** | PASS | Full end-to-end working prototype (Vite/React UI -> FastAPI -> ML Inference -> RAG). Local demo mode works deterministically. |
| **Fairness** | PASS | Documented in `docs/responsible-ai/RESPONSIBLE_AI.md` and frontend Responsible AI page. |
| **Transparency** | PASS | Model outputs include confidence scores and explicit warnings about demo/synthetic status. Citations are shown for RAG outputs. |
| **Ethics** | PASS | System acts as decision support, not a replacement for agronomists. |
| **Privacy** | PASS | No unnecessary PII (names, phone numbers, precise GPS) collected. |
| **Expected impact** | PASS | Documented in `README.md`. |
| **Impact statement** | PASS | Documented in `README.md`. |

*Note: The AI models use synthetic/demo data as permitted for a conceptual/working prototype. No fake real-world metrics are claimed.*
