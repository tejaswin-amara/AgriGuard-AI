# Runbook — Disaster Recovery

## Scope

Recreate the AgriGuard AI prototype from source after complete environment loss.

## Recovery sequence

### 1. Restore source

```bash
git clone https://github.com/tejaswin-amara/AgriGuard-AI.git
cd AgriGuard-AI
```

### 2. Restore configuration

```bash
cp .env.example .env
```

Populate only the credentials required for the chosen environment.

### 3. Restore database

Start PostgreSQL:

```bash
docker compose up -d db
```

Restore from the latest PostgreSQL backup when one exists.

### 4. Rebuild RAG state

```bash
python rag/ingestion/ingest.py
```

### 5. Rebuild the synthetic soil model

```bash
python models/soil/train.py
```

### 6. Start the application

```bash
docker compose up --build -d
```

## Recovery validation

Check:

- frontend loads;
- `GET /api/v1/health` responds;
- provider health endpoint responds;
- farm creation works;
- soil analysis works;
- disease demo accepts valid images;
- advisory generation respects the no-evidence boundary.

## Production note

There is currently no tested production-grade disaster-recovery environment, RPO, RTO, multi-region backup, or automated restore pipeline in the repository.
