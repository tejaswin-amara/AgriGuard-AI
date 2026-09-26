import os

import chromadb
from chromadb.utils import embedding_functions


class AdvisoryRetriever:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_db")
        self.client = chromadb.PersistentClient(path=db_path)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        try:
            self.collection = self.client.get_collection(
                "agri_advisory", embedding_function=self.ef
            )
        except Exception:  # noqa: BLE001
            self.collection = None

    def retrieve(self, query: str, n_results: int = 2):
        if not self.collection:
            return []

        results = self.collection.query(query_texts=[query], n_results=n_results)

        citations = []
        if results and results.get("documents") and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if results.get("metadatas") and i < len(results["metadatas"][0]) else {}

                citations.append(
                    {
                        "title": meta.get("title") or "Untitled Document",
                        "organization": meta.get("organization") or "Unknown Organization",
                        "content": doc,
                        "document_id": meta.get("id") or f"doc_{i}",
                        "url": meta.get("url"),  # None if missing; no fake fallback URL
                    }
                )
        return citations
