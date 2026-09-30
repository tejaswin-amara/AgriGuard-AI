# Threat Model

> This is a prototype threat model, not a security certification.

## Assets

- Farm records and coordinates.
- Soil readings and model outputs.
- Uploaded crop images during request processing.
- Advisory records and retrieved corpus text.
- IBM watsonx.ai credentials.
- PostgreSQL and MinIO credentials.
- RAG/vector-store contents.

## Threats and mitigations

| Threat | Current mitigation | Remaining gap |
|---|---|---|
| Malicious/oversized image upload | MIME allow-list + 10 MB limit | Deeper content scanning and authentication |
| Secret leakage | `.gitignore`, Gitleaks pre-commit/CI | No integrated production secret manager |
| External API failure | Provider cache, health checks, partial aggregation | Prototype fallbacks can return synthetic values |
| RAG prompt injection | Granite prompt treats retrieved text as passive reference | Retrieval corpus still needs stronger source governance |
| Unsupported advisory generation | No-evidence boundary | Corpus is currently tiny and demo-only |
| CORS misuse | Explicit configured CORS defaults | Production origin configuration must be reviewed |
| Dependency vulnerabilities | Trivy CI scan + Dependabot | Remediation is still an engineering responsibility |
| Unauthorized API access | None | Authentication/authorization not implemented |
| Abuse/rate exhaustion | None | Rate limiting/quotas not implemented |
| Model misuse | Explicit demo/synthetic limitation fields | UI/API consumers can still ignore warnings |

## Prototype data-integrity concerns

The current source still contains deterministic fallbacks in several provider paths. These must be treated as synthetic prototype values and not as observational truth.

## High-priority production work

Authentication, authorization, rate limiting, removal or explicit labeling of synthetic provider fallbacks, secure secret management, upload scanning, dependency patching, audit logging, and deployment hardening.
