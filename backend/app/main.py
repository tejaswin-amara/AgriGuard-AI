from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import advisory, disease, health, soil
from app.core.config import settings
from app.db.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=settings.project_name, lifespan=lifespan)

app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(disease.router, prefix=settings.api_v1_prefix)
app.include_router(soil.router, prefix=settings.api_v1_prefix)
app.include_router(advisory.router, prefix=settings.api_v1_prefix)
