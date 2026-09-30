# Deployment Architecture

## Current supported deployment

The repository is primarily a local/prototype deployment.

### Docker Compose

```text
Nginx/React :80
        |
        | /api/v1 is expected by the frontend client
        v
FastAPI :8000
   |        |
   v        v
Postgres  MinIO
```

ChromaDB is persisted within the application filesystem rather than as a separate service.

## Local prerequisites

- Docker Engine
- Docker Compose

## Startup

```bash
cp .env.example .env
docker compose up --build -d
```

## Current deployment caveats

1. The frontend container does not currently include a backend reverse-proxy configuration.
2. The backend is configured with development-oriented default credentials in Compose; these are not suitable for production.
3. Authentication and authorization are not implemented.
4. Production hosting, TLS termination, secrets management integration, backups, autoscaling, and multi-instance cache coordination are not implemented.
5. MinIO is provisioned, but the current disease upload service does not persist the uploaded bytes into MinIO.

## Production direction

A production deployment would need an authenticated API boundary, secret management, TLS, managed or hardened Postgres/object storage, background jobs for heavy inference where appropriate, centralized observability, rate limiting, migration orchestration, and a properly configured frontend/API routing layer.
