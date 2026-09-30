# Runbook — Rollback

## Scope

Return the repository or container deployment to a known source revision after a severe regression.

## Git rollback

Prefer a new revert commit on shared branches:

```bash
git log --oneline -10
git revert <bad-commit>
git push origin main
```

For local investigation only, a detached checkout of a previous known-good commit is safer than rewriting shared history.

## Docker rollback

The repository does not currently publish a versioned production image or deployment manifest. A rollback therefore means rebuilding from a selected Git revision:

```bash
git checkout <known-good-commit>
docker compose build
docker compose up -d
```

## Verify

Check:

```http
GET /api/v1/health
GET /api/v1/providers/health
```

Then run the backend tests and the frontend build/E2E suite.

## Do not

- force-push a shared rollback unless explicitly intended;
- claim a rollback is safe without a known-good revision;
- treat synthetic model/provider fallbacks as evidence of successful recovery.
