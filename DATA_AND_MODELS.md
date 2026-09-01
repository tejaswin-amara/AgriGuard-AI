# Data & Model Versioning

Neither `CLAUDE.md` nor `full-stack-dev-github-repos.md` covers this — both are scoped to the web pipeline plus a brief ML-tooling mention (MLflow, Airflow) for *tracking* experiments, not for *storing* the large binary files training actually produces. Filed here since it's a real gap, not an oversight to leave silent.

## The problem

A trained CNN checkpoint or an XGBoost model file is typically megabytes to hundreds of megabytes. Committing that directly to git bloats the repo permanently — git does not diff or garbage-collect binary blobs the way it does text, so the repo grows by the full file size on every retrain, forever. `.gitignore` in this repo already excludes `*.pt`, `*.pth`, `*.onnx`, `*.h5`, `*.pkl`, and `models/checkpoints/` for this reason.

## The fix: don't put them in git at all

| Option | When to use it |
|---|---|
| **[DVC](https://dvc.org/)** (Data Version Control) | The standard fit here — versions large files and datasets alongside git commits, storing the actual bytes in S3/MinIO/GCS instead of the git object store. Pairs naturally with the MinIO instance this project already runs (`docker-compose.yml`). |
| **Git LFS** | Simpler, more ubiquitous, GitHub-native. Less purpose-built for ML datasets than DVC, but lower setup cost if DVC feels like too much for a single model file. |
| **MLflow Model Registry** | Already adopted for experiment tracking (see `docs/TECHNICAL-ARCHITECTURE.md` Section 4.4) — it can also serve as the artifact store for trained weights, which may be enough without adding DVC on top. Reasonable to start here and add DVC only if dataset versioning (not just model versioning) becomes a real need. |

**Recommendation for this project's scale:** start with MLflow's own artifact store (already in the stack, zero new tooling). Add DVC only once there's a real, evolving dataset that itself needs versioning — not just the trained model output.

## What actually goes in git

- Training *scripts* (`models/`) — yes, these are code, version them normally
- Model *architecture* definitions — yes
- Trained *weights* — no, per above
- The advisory *corpus* (ICAR/state documents) — depends on size; a handful of PDFs can live in `models/corpus/` directly, a large corpus should follow the same DVC/external-storage pattern as model weights
