# Runbook — Incident Response

## Goal

Limit impact, preserve evidence, and restore the prototype to a known-good state.

## Incident categories

- API outage
- database outage
- external-provider outage
- LLM/provider failure
- security incident
- data-integrity issue

## Response

### 1. Triage

Record:

- timestamp;
- affected endpoint or service;
- current Git commit;
- workflow/CI status;
- provider health status.

### 2. Contain

For security or data-integrity incidents, stop unsafe flows before attempting a normal recovery.

Examples:

- disable external access if necessary;
- rotate exposed credentials;
- stop treating synthetic fallback data as observational data;
- preserve relevant logs and artifacts.

### 3. Recover

Use the relevant runbook:

- [dependency outage](dependency-outage.md)
- [external providers](external-provider-outages.md)
- [database restore](database-restore.md)
- [credential rotation](credential-rotation.md)
- [rollback](rollback.md)

### 4. Verify

Run:

```bash
cd backend
ruff check .
ruff format --check .
PYTHONPATH=. pytest tests/ -v
```

For frontend:

```bash
cd frontend
npm run lint
npm run build
npx playwright test
```

### 5. Document

Create or update the incident record with the failure mode, root cause, mitigation, and follow-up work.
