# Container Architecture

## Current local topology

Docker Compose defines four containers:

| Container | Base/runtime | Exposed port | Responsibility |
|---|---|---:|---|
| `frontend` | Node 22 build + Nginx Alpine runtime | 80 | Serves the compiled React application |
| `backend` | Python 3.12 slim | 8000 | FastAPI application and ML/RAG services |
| `db` | PostgreSQL 16 Alpine | 5432 | Relational application data |
| `minio` | MinIO | 9000 / 9001 | Object-storage service provisioned for local development |

## Internal application components

The backend process contains the provider adapters, cache/registry, risk engine, disease and soil services, RAG retrieval, and LLM provider abstraction.

ChromaDB uses local persistent storage under the `rag/` tree rather than a separate Compose service.

## Important boundary

The shipped frontend image uses a default Nginx configuration. The React API client calls relative `/api/v1` paths, but the repository does not currently ship an Nginx reverse-proxy rule that forwards those paths to the backend container. Therefore, the Docker topology is not evidence of a fully wired browser-to-API deployment by itself.
