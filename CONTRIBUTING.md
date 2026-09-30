# Contributing to AgriGuard AI

Thanks for contributing.

## Before you change code

Read:

- [README](README.md)
- [Technical Architecture](TECHNICAL-ARCHITECTURE.md)
- [AGENTS.md](AGENTS.md)
- relevant model cards and runbooks for the area you are touching.

The project is a prototype. Changes that make synthetic/demo data look like field-validated evidence are not acceptable.

## Development workflow

Create a branch from `main`:

```bash
git switch main
git pull
git switch -c feat/your-change
```

Use Conventional Commits for commit messages, for example:

```text
feat: add provider health detail
fix: correct advisory response contract
docs: update model limitations
```

## Backend checks

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd backend
ruff check .
ruff format --check .
PYTHONPATH=. pytest tests/ -v
```

## Frontend checks

```bash
cd frontend
npm ci
npm run lint
npm run build
npx playwright install --with-deps chromium
npx playwright test
```

## Pre-commit

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The hooks include Gitleaks, Ruff, formatting, YAML/file hygiene, and Biome formatting.

## Pull requests

Open a PR against `main` and complete the repository PR template.

A good PR should include:

- what changed and why;
- tests or verification performed;
- screenshots for meaningful frontend changes;
- security/privacy implications;
- documentation updates when behavior changes.

## Documentation rule

When code behavior changes, update the corresponding documentation in the same PR. In particular, keep these synchronized:

- API routes;
- demo instructions;
- architecture diagrams;
- model/data limitations;
- runbooks;
- changelog.

