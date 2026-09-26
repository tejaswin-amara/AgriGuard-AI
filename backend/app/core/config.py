"""Application settings, read from environment variables / .env.

See ../../.env.example at the repo root for the full list of variables
this project expects, with placeholder (non-secret) values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    project_name: str = "AgriGuard AI"
    api_v1_prefix: str = "/api/v1"

    # CORS Allowed Origins
    cors_origins: list[str] = [
        "http://localhost",
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ]

    # Database — see docker-compose.yml for the local Postgres service.
    database_url: str = "postgresql://agriguard:agriguard@localhost:5432/agriguard"

    # Object storage (MinIO) — for submitted leaf images.
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "agriguard-uploads"

    # LLM provider for the RAG advisory layer — IBM watsonx.ai / Granite.
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    granite_model_id: str = "ibm/granite-13b-instruct-v2"


settings = Settings()
