import time
from datetime import datetime, timezone
from app.services.external.base import ElevationProvider
from app.services.external.errors import ProviderResponseError
from app.services.external.transport import transport
from app.services.external.types import (
    DataQuality,
    ElevationData,
    FreshnessState,
    Provenance,
    ProviderStatusInfo,
)


class OpenTopoDataElevationProvider(ElevationProvider):
    provider_id = "open_topo_data"
    provider_name = "Open Topo Data Elevation API"
    is_required = False
    base_url = "https://api.opentopodata.org/v1/etopo1"

    async def get_elevation(self, lat: float, lon: float) -> ElevationData:
        params = {"locations": f"{round(lat, 4)},{round(lon, 4)}"}

        data = await transport.get_json(self.provider_id, self.base_url, params=params)
        if not isinstance(data, dict) or "results" not in data or not data["results"]:
            raise ProviderResponseError(self.provider_id, "Invalid response from Open Topo Data")

        result = data["results"][0]
        elev = float(result.get("elevation", 0.0))

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://www.opentopodata.org/",
            observed_at=datetime.now(timezone.utc),
            data_quality=DataQuality.REMOTE_SENSING,
            freshness=FreshnessState.FRESH,
            attribution="Open Topo Data / ETOPO1 Global Relief Model",
        )

        return ElevationData(
            elevation_m=round(elev, 1),
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        start = time.perf_counter()
        try:
            res = await transport.get_json(self.provider_id, self.base_url, params={"locations": "0,0"})
            latency = (time.perf_counter() - start) * 1000
            return ProviderStatusInfo(
                provider_id=self.provider_id,
                name=self.provider_name,
                category=self.category,
                is_required=self.is_required,
                enabled=True,
                status="healthy",
                latency_ms=round(latency, 1),
                last_success=datetime.now(timezone.utc),
            )
        except Exception as e:
            return ProviderStatusInfo(
                provider_id=self.provider_id,
                name=self.provider_name,
                category=self.category,
                is_required=self.is_required,
                enabled=True,
                status="unavailable",
                error_message=str(e),
                last_failure=datetime.now(timezone.utc),
            )
