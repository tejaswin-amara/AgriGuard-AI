# Runbook — Database and State Restore

## Scope

Recover local prototype state after data loss or environment recreation.

## PostgreSQL

The Docker Compose database uses the `db_data` named volume.

Inspect volumes:

```bash
docker volume ls
```

Create a logical backup:

```bash
docker compose exec db pg_dump -U agriguard agriguard > agriguard.sql
```

Restore into a running local database:

```bash
cat agriguard.sql | docker compose exec -T db psql -U agriguard agriguard
```

## ChromaDB RAG state

The vector database is derived state. It can be recreated from the Markdown corpus:

```bash
python rag/ingestion/ingest.py
```

Do not treat the generated `rag/vector_db/` directory as the source of truth.

## Soil model artifact

Regenerate the local synthetic model artifact:

```bash
python models/soil/train.py
```

## MinIO

Compose stores MinIO data in the `minio_data` named volume. A production system would need an explicit object-storage backup strategy.

## Database schema

The repository contains Alembic configuration and an initial revision, but the current application startup path creates SQLModel tables directly. Verify the active startup behavior before relying on Alembic as the sole restore mechanism.

## After restore

Validate:

```bash
GET /api/v1/health
GET /api/v1/providers/health
```

Then run the backend test suite.
