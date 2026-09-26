import time
from datetime import datetime, timezone

from app.services.external.base import GeocodingProvider
from app.services.external.errors import ProviderResponseError
from app.services.external.transport import transport
from app.services.external.types import (
    DataQuality,
    FreshnessState,
    GeocodedLocation,
    Provenance,
    ProviderStatusInfo,
)


class NominatimGeocodingProvider(GeocodingProvider):
    provider_id = "nominatim"
    provider_name = "Nominatim OpenStreetMap Geocoder"
    is_required = True
    search_url = "https://nominatim.openstreetmap.org/search"
    reverse_url = "https://nominatim.openstreetmap.org/reverse"

    async def geocode(self, query: str) -> GeocodedLocation:
        params = {
            "q": query,
            "format": "jsonv2",
            "addressdetails": 1,
            "limit": 1,
        }

        data = await transport.get_json(self.provider_id, self.search_url, params=params)
        if not isinstance(data, list) or len(data) == 0:
            raise ProviderResponseError(self.provider_id, f"No geocoding results found for query '{query}'")

        result = data[0]
        addr = result.get("address", {})

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://nominatim.openstreetmap.org/",
            observed_at=datetime.now(timezone.utc),
            data_quality=DataQuality.OFFICIAL_OBSERVATION,
            freshness=FreshnessState.FRESH,
            attribution="Data OpenStreetMap contributors",
        )

        return GeocodedLocation(
            name=query,
            display_name=result.get("display_name", query),
            latitude=float(result["lat"]),
            longitude=float(result["lon"]),
            country=addr.get("country"),
            state=addr.get("state"),
            district=addr.get("state_district") or addr.get("county"),
            city=addr.get("city") or addr.get("town"),
            village=addr.get("village") or addr.get("suburb"),
            provenance=provenance,
        )

    async def reverse_geocode(self, lat: float, lon: float) -> GeocodedLocation:
        params = {
            "lat": lat,
            "lon": lon,
            "format": "jsonv2",
            "addressdetails": 1,
        }

        data = await transport.get_json(self.provider_id, self.reverse_url, params=params)
        if not isinstance(data, dict) or "lat" not in data:
            raise ProviderResponseError(self.provider_id, f"Invalid reverse geocoding response for {lat},{lon}")

        addr = data.get("address", {})
        display_name = data.get("display_name", f"{lat:.4f}, {lon:.4f}")

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://nominatim.openstreetmap.org/",
            observed_at=datetime.now(timezone.utc),
            data_quality=DataQuality.OFFICIAL_OBSERVATION,
            freshness=FreshnessState.FRESH,
            attribution="Data OpenStreetMap contributors",
        )

        return GeocodedLocation(
            name=display_name.split(",")[0],
            display_name=display_name,
            latitude=float(data["lat"]),
            longitude=float(data["lon"]),
            country=addr.get("country"),
            state=addr.get("state"),
            district=addr.get("state_district") or addr.get("county"),
            city=addr.get("city") or addr.get("town"),
            village=addr.get("village") or addr.get("suburb"),
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        start = time.perf_counter()
        try:
            await transport.get_json(self.provider_id, self.search_url, params={"q": "Hyderabad", "format": "jsonv2", "limit": 1})
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
