import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

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
        # 1. Retrieve raw citations from ChromaDB corpus
        raw_citations = self.retriever.retrieve(query, n_results=3)

        citations: list[Citation] = []
        context_text = ""

        if weather_summary:
            context_text += f"Environmental Context: {weather_summary}\n"
        if risk_summary:
            context_text += f"Risk Indicators: {risk_summary}\n"

        for i, c in enumerate(raw_citations):
            citations.append(
                Citation(
                    title=c.get("title", "Agricultural Extension Bulletin"),
                    organization=c.get("organization", "Agricultural Extension Service"),
                    content=c.get("content", ""),
                    document_id=c.get("document_id", f"doc_{i+1}"),
                    url=c.get("url", "https://icar.org.in/"),
                    provider="ChromaDB Corpus",
                    source_type="knowledge_document",
                    data_quality="OFFICIAL_OBSERVATION",
                )
            )
            context_text += f"\nSource {i + 1} ({c['title']}): {c['content']}\n"

        # 2. Generate grounded response
        response = self.llm.generate(context=context_text, query=query)

        return {
            "recommendation": response["recommendation"],
            "provider": response["provider"],
            "citations": citations,
            "limitation": "Grounded advisory based on retrieved extension evidence. Field verification with an agronomist recommended.",
        }


rag_service = RAGService()
