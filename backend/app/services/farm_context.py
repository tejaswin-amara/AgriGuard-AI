import asyncio
import logging

from sqlmodel import Session

from app.models import Farm
from app.schemas import FarmContextResponse, FarmResponse
from app.services.external.cache import provider_cache
from app.services.external.providers import (
    AgricultureNewsProvider,
    GBIFBiodiversityProvider,
    NASAPowerClimateProvider,
    NominatimGeocodingProvider,
    OpenAQAirQualityProvider,
    OpenMeteoWeatherProvider,
    OpenTopoDataElevationProvider,
)
from app.services.external.providers.mock_providers import (
    MockClimateProvider,
    MockWeatherProvider,
)
from app.services.external.registry import provider_registry
from app.services.external.types import (
    AirQualityData,
    BiodiversityData,
    ElevationData,
    FreshnessState,
    GeocodedLocation,
    NewsData,
)
from app.services.risk_engine import risk_engine

logger = logging.getLogger("agriguard.services.farm_context")


class FarmContextService:
    def __init__(self):
        self.weather_provider = OpenMeteoWeatherProvider()
        self.climate_provider = NASAPowerClimateProvider()
        self.geocoding_provider = NominatimGeocodingProvider()
        self.air_quality_provider = OpenAQAirQualityProvider()
        self.elevation_provider = OpenTopoDataElevationProvider()
        self.biodiversity_provider = GBIFBiodiversityProvider()
        self.news_provider = AgricultureNewsProvider()

    async def get_or_create_farm_location(self, session: Session, farm: Farm) -> GeocodedLocation:
        cache_key = provider_cache.make_key("geocoding", farm.location_query)

        async def _fetch():
            try:
                return await self.geocoding_provider.geocode(farm.location_query)
            except Exception:
                return await self.geocoding_provider.reverse_geocode(farm.latitude, farm.longitude)

        loc, _ = await provider_cache.get_or_fetch(cache_key, _fetch, "geocoding")
        return loc

    async def get_farm_context(self, session: Session, farm: Farm) -> FarmContextResponse:
        lat, lon = farm.latitude, farm.longitude

        location = await self.get_or_create_farm_location(session, farm)

        weather_key = provider_cache.make_key("weather", lat=round(lat, 3), lon=round(lon, 3))
        climate_key = provider_cache.make_key("climate", lat=round(lat, 3), lon=round(lon, 3))
        aq_key = provider_cache.make_key("air_quality", lat=round(lat, 3), lon=round(lon, 3))
        elev_key = provider_cache.make_key("elevation", lat=round(lat, 3), lon=round(lon, 3))
        bio_key = provider_cache.make_key("biodiversity", lat=round(lat, 3), lon=round(lon, 3))
        news_key = provider_cache.make_key("news", query=farm.primary_crop)

        weather_task = provider_cache.get_or_fetch(
            weather_key, lambda: self.weather_provider.get_weather(lat, lon), "weather"
        )
        climate_task = provider_cache.get_or_fetch(
            climate_key, lambda: self.climate_provider.get_climate(lat, lon), "climate"
        )
        aq_task = provider_cache.get_or_fetch(
            aq_key, lambda: self.air_quality_provider.get_air_quality(lat, lon), "air_quality"
        )
        elev_task = provider_cache.get_or_fetch(
            elev_key, lambda: self.elevation_provider.get_elevation(lat, lon), "elevation"
        )
        bio_task = provider_cache.get_or_fetch(
            bio_key, lambda: self.biodiversity_provider.get_biodiversity(lat, lon), "biodiversity"
        )
        news_task = provider_cache.get_or_fetch(
            news_key, lambda: self.news_provider.get_news(farm.primary_crop), "news"
        )

        results = await asyncio.gather(
            weather_task, climate_task, aq_task, elev_task, bio_task, news_task, return_exceptions=True
        )

        weather, w_fresh = results[0] if not isinstance(results[0], Exception) else (None, FreshnessState.UNAVAILABLE)
        climate, c_fresh = results[1] if not isinstance(results[1], Exception) else (None, FreshnessState.UNAVAILABLE)
        air_quality, aq_fresh = results[2] if not isinstance(results[2], Exception) else (None, FreshnessState.UNAVAILABLE)
        elevation, e_fresh = results[3] if not isinstance(results[3], Exception) else (None, FreshnessState.UNAVAILABLE)
        biodiversity, b_fresh = results[4] if not isinstance(results[4], Exception) else (None, FreshnessState.UNAVAILABLE)
        news, n_fresh = results[5] if not isinstance(results[5], Exception) else (None, FreshnessState.UNAVAILABLE)

        if weather is None:
            weather = await MockWeatherProvider().get_weather(lat, lon)
            w_fresh = FreshnessState.STALE

        if climate is None:
            climate = await MockClimateProvider().get_climate(lat, lon)
            c_fresh = FreshnessState.STALE

        elevation_val = elevation.elevation_m if elevation else farm.elevation_m
        risk_ctx = risk_engine.evaluate(
            weather=weather,
            climate=climate,
            elevation_m=elevation_val,
        )

        provider_statuses = await provider_registry.get_health_status()

        freshness_map = {
            "weather": w_fresh.value,
            "climate": c_fresh.value,
            "geocoding": FreshnessState.FRESH.value,
            "air_quality": aq_fresh.value,
            "elevation": e_fresh.value,
            "biodiversity": b_fresh.value,
            "news": n_fresh.value,
        }

        farm_resp = FarmResponse(
            id=farm.id,
            name=farm.name,
            location_query=farm.location_query,
            latitude=farm.latitude,
            longitude=farm.longitude,
            elevation_m=elevation_val,
            timezone=farm.timezone,
            primary_crop=farm.primary_crop,
            plot_identifier=farm.plot_identifier,
            created_at=farm.created_at,
            updated_at=farm.updated_at,
        )

        return FarmContextResponse(
            farm=farm_resp,
            location=location,
            weather=weather,
            climate=climate,
            air_quality=air_quality if isinstance(air_quality, AirQualityData) else None,
            elevation=elevation if isinstance(elevation, ElevationData) else None,
            biodiversity=biodiversity if isinstance(biodiversity, BiodiversityData) else None,
            news=news if isinstance(news, NewsData) else None,
            risk_context=risk_ctx,
            provider_status=provider_statuses,
            freshness=freshness_map,
        )


farm_context_service = FarmContextService()
