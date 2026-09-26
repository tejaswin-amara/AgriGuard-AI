from app.services.external.providers.gbif import GBIFBiodiversityProvider
from app.services.external.providers.mock_providers import (
    MockAirQualityProvider,
    MockBiodiversityProvider,
    MockClimateProvider,
    MockElevationProvider,
    MockGeocodingProvider,
    MockNewsProvider,
    MockWeatherProvider,
)
from app.services.external.providers.nasa_power import NASAPowerClimateProvider
from app.services.external.providers.news import AgricultureNewsProvider
from app.services.external.providers.nominatim import NominatimGeocodingProvider
from app.services.external.providers.open_meteo import OpenMeteoWeatherProvider
from app.services.external.providers.open_topo_data import OpenTopoDataElevationProvider
from app.services.external.providers.openaq import OpenAQAirQualityProvider
from app.services.external.registry import provider_registry


def register_default_providers():
    """Register all core and optional provider adapters in the central registry."""
    provider_registry.register(OpenMeteoWeatherProvider())
    provider_registry.register(NASAPowerClimateProvider())
    provider_registry.register(NominatimGeocodingProvider())
    provider_registry.register(OpenAQAirQualityProvider())
    provider_registry.register(OpenTopoDataElevationProvider())
    provider_registry.register(GBIFBiodiversityProvider())
    provider_registry.register(AgricultureNewsProvider())


register_default_providers()

__all__ = [
    "AgricultureNewsProvider",
    "GBIFBiodiversityProvider",
    "MockAirQualityProvider",
    "MockBiodiversityProvider",
    "MockClimateProvider",
    "MockElevationProvider",
    "MockGeocodingProvider",
    "MockNewsProvider",
    "MockWeatherProvider",
    "NASAPowerClimateProvider",
    "NominatimGeocodingProvider",
    "OpenAQAirQualityProvider",
    "OpenMeteoWeatherProvider",
    "OpenTopoDataElevationProvider",
    "register_default_providers",
]
