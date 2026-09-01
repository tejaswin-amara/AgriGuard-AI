# Contributing to AgriGuard AI

Thanks for considering a contribution. This project follows the conventions below — please read before opening a PR.

## Reporting Bugs & Suggesting Features

Open a GitHub issue using the appropriate template:
- **Bug report** — for something broken
- **Feature request** — for something new

## Development Setup

See [`README.md`](README.md#project-structure-planned) for the planned project structure. Concrete setup steps will be added here once the backend scaffold lands — nothing to install yet.

## Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use for |
|---|---|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `docs:` | Documentation only |
| `chore:` | Tooling, dependencies, config |
| `refactor:` | Code change with no behavior change |

This is what keeps [`CHANGELOG.md`](CHANGELOG.md) generation automatable rather than hand-maintained.

## Pull Requests

1. Fork and branch from `main`
2. Keep PRs scoped to one change
3. Fill out the PR template
4. Reference the issue it closes, if any

## Code Review

Reviews follow [Google's Engineering Practices](https://github.com/google/eng-practices) — this project's own default for review standards. As author: keep PRs small and self-explanatory. As reviewer: focus on correctness and clarity, not style the linter should already catch.

## Responsible AI Contributions

Changes touching the model, the RAG corpus, or advisory copy should stay inside the [Responsible AI principles](README.md#responsible-ai) — most importantly: never let advisory output claim more confidence than the model actually has, and never add a new farmer data field without a clear, stated reason it needs to exist.
