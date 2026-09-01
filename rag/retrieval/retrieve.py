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
        except Exception:
            self.collection = None

    def retrieve(self, query: str, n_results: int = 2):
        if not self.collection:
            return []

        results = self.collection.query(query_texts=[query], n_results=n_results)

        citations = []
        if results["documents"] and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if results["metadatas"] else {}

                citations.append(
                    {
                        "title": meta.get("title", "Unknown Source"),
                        "organization": meta.get("organization", "Unknown"),
                        "content": doc,
                        "document_id": meta.get("id", f"doc_{i}"),
                    }
                )
        return citations
