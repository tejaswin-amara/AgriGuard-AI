from rag.retrieval.retrieve import AdvisoryRetriever

from app.schemas import Citation
from app.services.llm import get_llm_provider


class RAGService:
    def __init__(self):
        self.retriever = AdvisoryRetriever()
        self.llm = get_llm_provider()

    def generate_advisory(
        self,
        query: str,
        weather_summary: str | None = None,
        risk_summary: str | None = None,
    ) -> dict:
        raw_citations = self.retriever.retrieve(query, n_results=3)

        if not raw_citations:
            return {
                "recommendation": "No authoritative agricultural extension evidence was retrieved for this query. "
                "Please consult a certified local agronomist or extension officer for field guidance.",
                "provider": "rag-grounding-boundary",
                "citations": [],
                "limitation": "Insufficient retrieved evidence to make a grounded recommendation.",
            }

        citations: list[Citation] = []
        context_text = ""

        if weather_summary:
            context_text += f"Environmental Context: {weather_summary}\n"
        if risk_summary:
            context_text += f"Risk Indicators: {risk_summary}\n"

        for i, c in enumerate(raw_citations):
            citations.append(
                Citation(
                    title=c.get("title") or "Agricultural Extension Bulletin",
                    organization=c.get("organization") or "Unknown Organization",
                    content=c.get("content", ""),
                    document_id=c.get("document_id") or f"doc_{i + 1}",
                    url=c.get("url"),  # None if missing, never fabricate URLs
                    provider="ChromaDB Corpus",
                    source_type="knowledge_document",
                    data_quality="OFFICIAL_OBSERVATION",
                )
            )
            title_str = c.get("title") or "Extension Document"
            context_text += f"\n--- RETRIEVED DOCUMENT {i + 1} ({title_str}) ---\n{c.get('content', '')}\n--- END DOCUMENT {i + 1} ---\n"

        response = self.llm.generate(context=context_text, query=query)

        return {
            "recommendation": response["recommendation"],
            "provider": response["provider"],
            "citations": citations,
            "limitation": "Grounded advisory based on retrieved extension evidence. Field verification with an agronomist recommended.",
        }


rag_service = RAGService()
