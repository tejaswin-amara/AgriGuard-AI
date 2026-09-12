import os
import sys

# Add root to sys path so we can import rag module
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

    def generate_advisory(self, query: str) -> dict:
        # Retrieve context
        raw_citations = self.retriever.retrieve(query)

        citations = []
        context_text = ""
        for i, c in enumerate(raw_citations):
            citations.append(Citation(**c))
            context_text += f"\nSource {i + 1} ({c['title']}): {c['content']}\n"

        # Generate answer grounded in context
        response = self.llm.generate(context=context_text, query=query)

        return {
            "recommendation": response["recommendation"],
            "provider": response["provider"],
            "citations": citations,
        }
