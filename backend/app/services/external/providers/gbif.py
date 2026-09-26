import time
from datetime import datetime, timezone

from app.services.external.base import BiodiversityProvider
from app.services.external.transport import transport
from app.services.external.types import (
    BiodiversityData,
    BiodiversityObservation,
    DataQuality,
    FreshnessState,
    Provenance,
    ProviderStatusInfo,
)


class GBIFBiodiversityProvider(BiodiversityProvider):
    provider_id = "gbif"
    provider_name = "GBIF Species Occurrence API"
    is_required = False
    base_url = "https://api.gbif.org/v1/occurrence/search"

    async def get_biodiversity(self, lat: float, lon: float) -> BiodiversityData:
        lat_min, lat_max = round(lat - 0.2, 3), round(lat + 0.2, 3)
        lon_min, lon_max = round(lon - 0.2, 3), round(lon + 0.2, 3)

        params = {
            "decimalLatitude": f"{lat_min},{lat_max}",
            "decimalLongitude": f"{lon_min},{lon_max}",
            "limit": 10,
        }

        data = await transport.get_json(self.provider_id, self.base_url, params=params)
        observations: list[BiodiversityObservation] = []
        total = 0

        if isinstance(data, dict):
            total = data.get("count", 0)
            results = data.get("results", [])
            for r in results:
                species = r.get("species") or r.get("scientificName") or "Unknown Species"
                vernacular = r.get("vernacularName")
                kingdom = r.get("kingdom", "General")
                event_date = r.get("eventDate")
                dataset = r.get("datasetName")

                observations.append(
                    BiodiversityObservation(
                        species_name=species,
                        common_name=vernacular,
                        category=kingdom.lower(),
                        observation_count=1,
                        last_observed_at=event_date,
                        dataset=dataset,
                    )
                )

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://www.gbif.org/",
            observed_at=datetime.now(timezone.utc),
            data_quality=DataQuality.OFFICIAL_OBSERVATION,
            freshness=FreshnessState.FRESH,
            attribution="Data from Global Biodiversity Information Facility (GBIF)",
        )

        return BiodiversityData(
            total_observations=total,
            observations=observations,
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        start = time.perf_counter()
        try:
            await transport.get_json(self.provider_id, self.base_url, params={"limit": 1})
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
