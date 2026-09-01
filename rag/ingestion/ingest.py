import os
import re
import chromadb
from chromadb.utils import embedding_functions


def parse_markdown_with_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple regex to extract frontmatter
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        frontmatter_str = match.group(1)
        body = match.group(2).strip()

        metadata = {}
        for line in frontmatter_str.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                metadata[key.strip()] = val.strip().strip('"')

        return metadata, body
    return {}, content


def ingest_corpus():
    # Setup ChromaDB
    # We use a persistent client in the rag directory
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_db")
    client = chromadb.PersistentClient(path=db_path)

    # Use a lightweight sentence-transformer model
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="agri_advisory", embedding_function=sentence_transformer_ef
    )

    corpus_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "corpus")

    documents = []
    metadatas = []
    ids = []

    for filename in os.listdir(corpus_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(corpus_dir, filename)
            meta, body = parse_markdown_with_frontmatter(file_path)

            # Simple chunking: one chunk per document for this small demo corpus
            doc_id = meta.get("id", filename)

            documents.append(body)
            # Ensure metadata values are str, int, float or bool
            clean_meta = {k: str(v) for k, v in meta.items()}
            metadatas.append(clean_meta)
            ids.append(f"{doc_id}_chunk1")

    if documents:
        collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Ingested {len(documents)} documents into ChromaDB at {db_path}")


if __name__ == "__main__":
    ingest_corpus()
