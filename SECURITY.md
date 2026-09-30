# Security Policy

## Project status

AgriGuard AI is a public student/project prototype. There are no published production releases at the time of this policy revision.

## Reporting a vulnerability

Do not open a public GitHub issue for a security-sensitive vulnerability.

Use GitHub's private vulnerability reporting when available, or contact the project maintainer through the private contact channel configured for the repository.

Include:

- affected file or endpoint;
- reproduction steps;
- expected and observed behavior;
- potential impact;
- any suggested mitigation.

Do not include real credentials in a report.

## Current security controls

The repository currently includes:

- image MIME-type validation;
- 10 MB image-size validation;
- explicit default CORS origins;
- Pydantic input constraints;
- Gitleaks pre-commit/CI scanning;
- Trivy repository/image scanning;
- Dependabot configuration;
- provenance and limitation metadata;
- prompt-boundary wording for retrieved RAG text.

## Current security gaps

The current application does **not** yet implement:

- authentication or authorization;
- rate limiting;
- production secret-manager integration;
- upload malware/content scanning;
- comprehensive audit logging;
- hardened production TLS/deployment configuration.

The farm model currently stores resolved latitude/longitude because location is used to retrieve environmental context. Therefore documentation should not claim that the application collects “no precise GPS” data.

Local Compose credentials are development defaults only and must not be reused in production.

## Secret handling

Use `.env` for local development and keep it untracked.

Never commit:

- IBM watsonx.ai API keys;
- database passwords;
- MinIO credentials;
- private tokens;
- credential-bearing logs.

Gitleaks should be run before pushing changes.

