from fastapi import APIRouter

from app.services.external.registry import provider_registry

router = APIRouter()


@router.get("/health", summary="Application & System Health", tags=["Health"])
async def health_check():
    provider_statuses = await provider_registry.get_health_status()
    unhealthy = [p.name for p in provider_statuses if p.is_required and p.status != "healthy"]

    return {
        "status": "healthy" if not unhealthy else "degraded",
        "service": "AgriGuard AI Platform",
        "version": "2.0.0",
        "degraded_required_providers": unhealthy,
    }
