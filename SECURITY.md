# Security Policy

## Supported Versions

Pre-1.0 — only the `main` branch is supported. There are no tagged releases yet.

## Reporting a Vulnerability

Please **do not** open a public issue for a security concern. Instead:
- Use GitHub's private vulnerability reporting (Security tab → Report a vulnerability), or
- Email tejaswinamara@klh.edu.in directly

Please include what you found and where, steps to reproduce, and potential impact if known.

## Response

This is a student project without a formal SLA, but reports will be acknowledged and addressed as promptly as possible.

## Scope Notes

- **Farmer data** — only crop images and soil readings are collected, no names, phone numbers, or precise location (see the Responsible AI section in [`README.md`](README.md#responsible-ai)). A report involving unintended collection or exposure of more than that is treated as high priority.
- **Secrets** — API keys and database credentials are managed via Infisical, never committed; `gitleaks` runs in CI to catch accidental leaks. Full reasoning in [`docs/TECHNICAL-ARCHITECTURE.md`](docs/TECHNICAL-ARCHITECTURE.md).
