from fastapi import APIRouter

from app.services.external.registry import provider_registry
from app.services.external.types import ProviderStatusInfo

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("", response_model=list[ProviderStatusInfo], summary="List Registered Providers & Status")
async def list_providers():
    return await provider_registry.get_health_status()


@router.get("/health", response_model=list[ProviderStatusInfo], summary="Check Health of All Providers")
async def check_providers_health():
    return await provider_registry.get_health_status()
