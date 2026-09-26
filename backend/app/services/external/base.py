from abc import ABC, abstractmethod
from typing import Any
from app.services.external.types import (
    AirQualityData,
    BiodiversityData,
    ClimateData,
    ElevationData,
    GeocodedLocation,
    NewsData,
    ProviderStatusInfo,
    WeatherData,
)


class ExternalDataProvider(ABC):
    provider_id: str
    provider_name: str
    category: str
    is_required: bool = False

    @abstractmethod
    async def health_check(self) -> ProviderStatusInfo:
        """Check if provider endpoint is responsive."""
        pass


class WeatherProvider(ExternalDataProvider):
    category = "weather"

    @abstractmethod
    async def get_weather(self, lat: float, lon: float) -> WeatherData:
        pass


class ClimateProvider(ExternalDataProvider):
    category = "climate"

    @abstractmethod
    async def get_climate(self, lat: float, lon: float) -> ClimateData:
        pass


class GeocodingProvider(ExternalDataProvider):
    category = "geocoding"

    @abstractmethod
    async def geocode(self, query: str) -> GeocodedLocation:
        pass

    @abstractmethod
    async def reverse_geocode(self, lat: float, lon: float) -> GeocodedLocation:
        pass


class AirQualityProvider(ExternalDataProvider):
    category = "air_quality"

    @abstractmethod
    async def get_air_quality(self, lat: float, lon: float) -> AirQualityData:
        pass


class ElevationProvider(ExternalDataProvider):
    category = "elevation"

    @abstractmethod
    async def get_elevation(self, lat: float, lon: float) -> ElevationData:
        pass


class BiodiversityProvider(ExternalDataProvider):
    category = "biodiversity"

    @abstractmethod
    async def get_biodiversity(self, lat: float, lon: float) -> BiodiversityData:
        pass


class NewsProvider(ExternalDataProvider):
    category = "news"

    @abstractmethod
    async def get_news(self, query: str = "agriculture") -> NewsData:
        pass
