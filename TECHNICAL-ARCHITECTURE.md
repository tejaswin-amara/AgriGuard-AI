# AgriGuard AI — Technical Architecture & Build Plan

**Companion to:** `AgriGuard-AI-1M1B-Submission.pptx`
**This revision:** goes through `CLAUDE.md` and `full-stack-dev-github-repos.md` end to end — every category in both documents gets an explicit call: adopted, situational (add later), or not applicable. Nothing is skipped silently.

---

## Revision Note

The first pass of this document defaulted to a TypeScript backend (`create-t3-app` + Prisma) because that's `CLAUDE.md`'s first-listed web scaffold. Going through the full list properly surfaced a better-fitting default: the actual workload here is Python ML (a CNN and a gradient-boosted tree), and `full-stack-dev-github-repos.md` is explicit that `fastapi/full-stack-fastapi-template` is *"the natural pick when the backend needs to be Python instead of TypeScript."* That's this project, not an edge case of it. This revision corrects the backend and data-layer picks throughout.

**Second correction, this pass:** the LLM/RAG provider was Anthropic's SDK — a defensible general pick, but it missed something specific to *this* project: the 1M1B guideline document's own "Allowed AI Components" list names IBM Granite Models directly, and this internship runs in partnership with IBM SkillsBuild. Section 4.4 now defaults to `ibm-watsonx-ai` (verified installable) instead. Neither correction was caught by re-reading more carefully — both surfaced by going back to source documents (the reference repo lists, the original 1M1B brief) that were already sitting in this conversation and checking the pick against them properly, rather than assuming the first pass had it right.

## 1. Project Summary

AI-assisted crop disease and soil health advisory for smallholder Indian farmers: an image-based disease classifier, a tabular soil-health model, and a RAG-grounded layer that phrases both into plain-language, source-cited recommendations.

## 2. Data Sources (Planned — Not Yet Finalized)

| Component | Planned source | Status |
|---|---|---|
| Disease detection | Open leaf-image datasets in the PlantVillage family, or an India-specific crop image collection if accessible | Starting point — swap for your actual dataset |
| Soil health | Tabular N-P-K, pH, moisture, rainfall — parameters aligned with what India's Soil Health Card scheme reports | Exact source TBD |
| Advisory grounding | ICAR and state agricultural department advisory publications, chunked into a retrieval corpus | To be assembled |

These are scoping assumptions, not measured facts — see Section 9 for exactly what to swap in once your real dataset and results are locked.

## 3. Model Architecture

| Component | Approach | Note |
|---|---|---|
| Disease Detection | Transfer-learning CNN — EfficientNet-B0 or ResNet-50 backbone, fine-tuned on labeled leaf imagery | Swap backbone freely; a defensible starting point, not a fixed requirement |
| Soil Health Advisory | Gradient-boosted trees — XGBoost or Random Forest on tabular soil parameters | Classification (risk tier) or regression (dosage) depending on framing |
| Grounded Advisory Layer | RAG — embed the advisory corpus, retrieve top-k passages, feed as context to an LLM prompt that phrases the final recommendation | Makes "Transparency" concrete instead of a slide-only claim |

## 4. Full Tech Stack — Complete Mapping

Organized in the pipeline order the reference doc itself uses: foundations → scaffold/structure → frontend → data/AI/background work → security/testing/ops → beyond-web-app → agent tooling. Every row states adopted / situational / not applicable, so the full list has been considered on purpose, not cherry-picked.

### 4.1 Foundations

| Task | Choice | Call |
|---|---|---|
| License | `github/choosealicense.com` → MIT | **Adopted** — permissive, fits a project likely to be shared or open-sourced as part of the internship |
| Git reference | `progit/progit2` | Adopted — standard reference |
| Commit format | Conventional Commits | Adopted — `feat:`/`fix:`/`chore:` from day one |
| Task tracking | `makeplane/plane` | Situational — once more than one person (e.g. an Origins teammate) contributes |
| Contribution docs | `github/opensource.guide` | Situational — write a CONTRIBUTING.md if the repo goes public |
| Code review standard | `google/eng-practices` | Situational — applies once a second reviewer exists |
| Workflow automation | `n8n-io/n8n` | Situational, real fit — wiring the finished advisory to an actual delivery channel (SMS/WhatsApp notification) without hand-coding each integration; source-available license, keep any self-hosted instance patched |
| Index for anything uncovered | `sindresorhus/awesome` | Adopted as fallback — start here for anything this table doesn't answer |

### 4.2 Scaffold & Structure

| Task | Choice | Call |
|---|---|---|
| Backend & inference API | `fastapi/full-stack-fastapi-template` | **Adopted — corrected pick.** Ships FastAPI + React + SQLModel + PostgreSQL + Docker Compose + CI already wired together; Python-native, no bridge needed to call the CNN/tree model |
| ML package scaffold | `cookiecutter/cookiecutter` | Situational — if model-training code is split into its own installable Python package, separate from the API repo |
| Frontend structure | `alan2207/bulletproof-react` | Adopted — for the React frontend the FastAPI template ships with |
| Reference implementations | `gothinkster/realworld`, `spring-petclinic-reactjs` | Not adopted — generic CRUD reference, low transfer value for an ML-advisory tool |
| Monorepo | `t3-oss/create-t3-turbo` | Not needed yet — only relevant if a genuinely separate mobile app or shared package appears later |

### 4.3 Frontend

| Task | Choice | Call |
|---|---|---|
| UI components | `shadcn-ui/ui` | Adopted — edit component source directly |
| Accessibility | `dequelabs/axe-core` | **Adopted, elevated priority** — low-end devices and screen-reader use are a real part of this user base, not an edge case |
| Internationalization | `i18next` + `react-i18next` | **Adopted, elevated priority** — most end users won't read English; close to a hard requirement for the stated target users |
| Forms & validation | `react-hook-form` + `colinhacks/zod` | Adopted — validates the soil-reading form (NPK, pH, moisture) before it reaches the model |
| Server-state | `TanStack/query` | Adopted — caching/refetching against the FastAPI endpoints |
| Real-time | `socketio/socket.io` | Situational — only if a live "analyzing your photo..." status or a chat-style interface gets built |
| Animation | `motiondivision/motion` | Not adopted — polish, not core, for a utilitarian advisory tool |
| Component docs | `storybookjs/storybook` | Situational — once the component set outgrows ad hoc screenshots |

### 4.4 Data, AI & Background Work

| Task | Choice | Call |
|---|---|---|
| Database / ORM | SQLModel + PostgreSQL | **Adopted — corrected from Prisma**, which is TypeScript-only and doesn't fit a Python backend; SQLModel ships with the FastAPI template |
| AI/LLM orchestration | **IBM watsonx.ai + Granite models** (`ibm-watsonx-ai` SDK, verified installable — v1.7.1 as of this writing) | **Corrected pick, second pass.** The first two passes of this document defaulted to Anthropic's SDK, which is a reasonable general-purpose choice but misses something specific to this project: the 1M1B guideline document itself, under "Allowed AI Components," names IBM Granite Models explicitly — and this internship runs in partnership with IBM SkillsBuild. `ibm-watsonx-ai` has native RAG support (LangChain/Chroma integration, a purpose-built `RAG` extension module) and Granite Guardian for groundedness/relevance detection, which maps directly onto this project's own "never state an ungrounded recommendation" rule. Any other provider, Anthropic included, remains a valid fallback — just not the contextually correct default here. |
| `vercel/ai` | — | Situational only — relevant if a separate Node/Next.js edge layer is added later for client-side streaming; not needed in this architecture |
| Background jobs | `taskforcesh/bullmq` | **Gap, flagged honestly** — BullMQ is Node/Redis-specific and doesn't fit an all-Python backend. Celery or RQ are the standard Python equivalents; neither is in this project's list, so picked here per `CLAUDE.md`'s own rule that an uncovered task gets a normal pick, not a forced fit. Real use case: queuing photo-classification jobs so a slow rural connection isn't left waiting on a blocking request |
| Auth | `better-auth/better-auth` | **Same kind of gap** — TypeScript-only, doesn't fit the Python backend. `fastapi-users` or the JWT pattern the FastAPI template itself typically bundles is the natural in-ecosystem pick instead |
| Object storage | `minio/minio` | Adopted — stores submitted leaf images for audit trail / future retraining, self-hosted |
| Caching | `redis/redis` | Situational — cache repeated RAG queries once traffic justifies it |
| Search | `meilisearch/meilisearch` | Situational — only if officers/NGOs need to browse the advisory corpus by keyword, separate from RAG retrieval itself |
| Data transformation | `dbt-labs/dbt-core` | Situational, real fit — once district-level aggregated soil trends (the secondary "extension officer" use case from the deck) become a proper reporting layer |
| Data pipeline orchestration | `apache/airflow` | Situational — only once data cleaning becomes multi-stage with real retry/scheduling needs |
| Experiment tracking | `mlflow/mlflow` | Adopted — tracks model versions/params/metrics as the CNN and tree model get iterated on |

### 4.5 Security, Testing & Ops

| Task | Choice | Call |
|---|---|---|
| Secrets management | `gitleaks/gitleaks` (scan) + `Infisical/infisical` (manage) | **Adopted** — keeps the LLM API key and DB credentials out of a public student GitHub repo, a genuinely common student mistake |
| Security review | `OWASP/CheatSheetSeries` | Adopted — input validation + auth cheat sheets before any public deployment |
| API documentation | `scalar/scalar` | Adopted — FastAPI auto-generates OpenAPI; Scalar gives it a cleaner reference UI essentially for free |
| E2E testing | `cypress-io/cypress-realworld-app` (pattern) | Adopted — once the upload-photo → get-advisory flow is real, not before |
| CI/CD | `actions/starter-workflows` | Adopted — partly pre-wired by the FastAPI template already |
| Containerize | `docker/awesome-compose` | Adopted — local dev: FastAPI + Postgres + MinIO in one Compose file |
| Hosting | `ripienaar/free-for-dev` | Adopted — verify current free-tier limits before committing, per the source doc's own drift warning |
| Analytics | `umami-software/umami` | Adopted — tracks which crops/regions generate queries, self-hosted and cookieless, consistent with the Privacy principle already stated in the deck |
| Infra as code | `opentofu/opentofu` (not Terraform) | Not needed yet — noted now so Terraform isn't defaulted to out of habit once it does matter |
| Load testing | `grafana/k6` | Not needed yet — revisit if real farmer-scale traffic arrives |
| API gateway | `Kong/kong` | Not applicable at this scale — single backend service |
| Event streaming | `nats-io/nats-server`, `apache/kafka` | Not applicable at this scale |
| Headless CMS | `payloadcms/payload` | Situational, real fit — worth considering if non-engineers (Origins members, agri-extension partners) need to curate the advisory corpus without touching code |
| Scaling reference | `donnemartin/system-design-primer` | Situational — once real adoption creates real load |
| Study a production app | `calcom/cal.diy` | Not adopted — different domain (scheduling), low transfer value here |
| "Go deeper" | `codecrafters-io/build-your-own-x` | Optional — its build-your-own-vector-database challenge is genuinely relevant background for understanding what the RAG layer does internally |

### 4.6 Beyond a Typical Web App

| Task | Choice | Call |
|---|---|---|
| Payments | `medusajs/medusa`, `getlago/lago` | Not applicable — no commerce or billing feature in this project |
| Desktop | `tauri-apps/tauri`, `electron/electron` | Not applicable — a farmer-facing tool has no reason to be a desktop app |
| Native mobile | `facebook/react-native` or `flutter/flutter` | **Situational, real consideration** — most farmers reach this on mid/low-end Android over patchy connectivity. If an installable, offline-capable PWA (buildable from the same React frontend) isn't enough — especially for queuing photo uploads while offline — this is a genuine next step, not boilerplate advice |

### 4.7 If An AI Agent Keeps Building This

This project has been agent-assisted from the start, so the reference doc's own "Bonus" section applies directly:

| Task | Choice | Call |
|---|---|---|
| Skill pack | `anthropics/skills` | Adopted — official, conservative baseline for continued Claude Code-style work |
| Pre-push validation | `kunchenguid/no-mistakes` | Situational — a real, low-cost safety net given how this project originated |
| Design skill | `emilkowalski/skills` (apple-design) | Situational — for frontend polish once the core flow works |
| Agent memory/governance | `DeusData/codebase-memory-mcp`, `microsoft/agent-governance-toolkit` | Not needed at this scale |

## 5. Responsible AI — Implementation Notes

More concrete than the deck's summary slide:

- **Fairness** — audit dataset class balance by crop and region before training; report under-represented categories rather than assuming neutrality.
- **Transparency** — every recommendation ships with its confidence score and the retrieved advisory passage it was grounded in. No bare AI verdict.
- **Ethics** — low-confidence or high-stakes outputs route to a "consult an agronomist" message rather than a confidently-phrased auto-recommendation.
- **Privacy** — only crop images and soil readings are collected; no name, phone number, or precise GPS. Aggregate any location data to district level only.
- **Access, not just output** — the i18n and accessibility picks in Section 4.3 belong here too: a technically fair model that only a subset of literate, English-reading users can actually operate isn't fully serving the stated target users.

## 6. Prototype Flow

1. **Input** — farmer submits a leaf photo or a soil reading (N-P-K, pH, moisture) through a simple form.
2. **Inference** — the CNN or tree model scores the input, returns a category and confidence.
3. **Grounding** — the raw result is matched against the ICAR/state advisory corpus via RAG retrieval.
4. **Output** — an LLM call phrases the grounded result into a plain-language recommendation, source cited.

## 7. Assumptions & What To Customize

Nothing here reflects a real dataset, trained model, or measured result — replace before treating this as a finished build plan:

| Placeholder in this doc | Replace with |
|---|---|
| PlantVillage-style / Soil Health Card-style dataset framing | The actual dataset(s) you're training on |
| EfficientNet/ResNet, XGBoost as "planned approach" | Your actual model architecture, if different |
| No accuracy figures given anywhere | Real metrics once you have them — never placeholder numbers presented as measured |
| "Conceptual" framing throughout | Update to "working prototype" language once a real demo exists |

## 8. Where This Sits in the 1M1B Deliverable

The 1M1B guideline document explicitly accepts a **conceptual or working prototype** — flow diagrams count as a valid "Prototype/Demo" element. Nothing here requires a fully trained, deployed system to be submission-ready. This document exists so the build, if and when it goes further, doesn't start from a blank page — and now reflects the full breadth of this project's own tool defaults, not just the first-listed option in each category.
