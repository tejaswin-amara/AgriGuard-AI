"""Application settings, read from environment variables / .env.

See ../../.env.example at the repo root for the full list of variables
this project expects, with placeholder (non-secret) values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    project_name: str = "AgriGuard AI"
    api_v1_prefix: str = "/api/v1"

    # Database — see docker-compose.yml for the local Postgres service.
    database_url: str = "postgresql://agriguard:agriguard@localhost:5432/agriguard"

    # Object storage (MinIO) — for submitted leaf images.
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "agriguard-uploads"

    # LLM provider for the RAG advisory layer — IBM watsonx.ai / Granite,
    # per docs/TECHNICAL-ARCHITECTURE.md Section 4.4. Get real values from
    # https://dataplatform.cloud.ibm.com/ (API key + project_id). Never
    # commit real values — this is read from the environment / a local
    # .env that stays gitignored.
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    # Granite model naming moves fast (3.x -> 4.0 within the last year alone).
    # Don't trust this default — check the current list before using it:
    # https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-api-model-ids.html
    granite_model_id: str = "CHECK_CURRENT_MODEL_LIST_BEFORE_USING"


settings = Settings()
