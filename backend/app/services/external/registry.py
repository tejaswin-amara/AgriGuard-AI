import asyncio
import logging
from typing import Any
from app.services.external.base import ExternalDataProvider
from app.services.external.types import ProviderStatusInfo

logger = logging.getLogger("agriguard.external.registry")


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, ExternalDataProvider] = {}

    def register(self, provider: ExternalDataProvider):
        self._providers[provider.provider_id] = provider
        logger.info(f"Registered external provider: {provider.provider_id} ({provider.provider_name})")

    def get(self, provider_id: str) -> ExternalDataProvider | None:
        return self._providers.get(provider_id)

    def get_by_category(self, category: str) -> list[ExternalDataProvider]:
        return [p for p in self._providers.values() if p.category == category]

    async def get_health_status(self) -> list[ProviderStatusInfo]:
        tasks = [p.health_check() for p in self._providers.values()]
        if not tasks:
            return []
        results = await asyncio.gather(*tasks, return_exceptions=True)
        statuses = []
        for p, res in zip(self._providers.values(), results):
            if isinstance(res, Exception):
                statuses.append(
                    ProviderStatusInfo(
                        provider_id=p.provider_id,
                        name=p.provider_name,
                        category=p.category,
                        is_required=p.is_required,
                        enabled=True,
                        status="unavailable",
                        error_message=str(res),
                    )
                )
            elif isinstance(res, ProviderStatusInfo):
                statuses.append(res)
        return statuses


provider_registry = ProviderRegistry()
