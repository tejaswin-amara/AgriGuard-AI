from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    advisory,
    biodiversity,
    disease,
    environment,
    farm,
    health,
    location,
    news,
    providers,
    soil,
    weather,
)
from app.core.config import settings
from app.db.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.project_name,
    version="2.0.0",
    description="AgriGuard AI — Context-Aware Agricultural Intelligence & Advisory Platform",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

# Configure CORS restricted to configured allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all route modules with API V1 prefix
app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(farm.router, prefix=settings.api_v1_prefix)
app.include_router(location.router, prefix=settings.api_v1_prefix)
app.include_router(weather.router, prefix=settings.api_v1_prefix)
app.include_router(environment.router, prefix=settings.api_v1_prefix)
app.include_router(providers.router, prefix=settings.api_v1_prefix)
app.include_router(news.router, prefix=settings.api_v1_prefix)
app.include_router(biodiversity.router, prefix=settings.api_v1_prefix)
app.include_router(disease.router, prefix=settings.api_v1_prefix)
app.include_router(soil.router, prefix=settings.api_v1_prefix)
app.include_router(advisory.router, prefix=settings.api_v1_prefix)
