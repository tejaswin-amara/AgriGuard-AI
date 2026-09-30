# Runbook — Credential Rotation

## Scope

Rotate secrets used by local or future deployed AgriGuard AI instances.

## Credentials currently represented

- PostgreSQL connection string / credentials
- MinIO access credentials
- IBM watsonx.ai API key
- IBM watsonx.ai project ID

## Current storage mechanism

Local configuration is loaded from `.env`, based on `.env.example`. The repository does **not** currently integrate a production secret manager.

## Procedure

1. Stop services that hold the old secret.
2. Generate a new credential in the upstream system.
3. Update the local `.env` or deployment secret store.
4. Restart the affected service.
5. Validate:
   - `GET /api/v1/health`
   - `GET /api/v1/providers/health`
   - relevant database/API operations
6. Revoke the old credential after the new credential is confirmed.
7. Run Gitleaks before committing any configuration changes.

## Never commit

Do not commit:

- `.env`
- real API keys
- production database passwords
- production MinIO credentials
- credential-bearing logs

