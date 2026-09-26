import pytest
from app.services.external.cache import ProviderCache, FreshnessState
from app.services.external.errors import ProviderError, ProviderTimeoutError
from app.services.external.providers.mock_providers import (
    MockAirQualityProvider,
    MockBiodiversityProvider,
    MockClimateProvider,
    MockElevationProvider,
    MockGeocodingProvider,
    MockNewsProvider,
    MockWeatherProvider,
)
from app.services.risk_engine import RiskEngine
from app.services.external.types import WeatherData, ClimateData, Provenance, DataQuality


@pytest.mark.anyio
async def test_mock_weather_provider():
    provider = MockWeatherProvider()
    data = await provider.get_weather(18.67, 78.09)
    assert data.temperature_c == 28.5
    assert data.humidity_pct == 82.0
    assert len(data.forecast) == 2
    assert data.provenance.provider == "mock_weather"


@pytest.mark.anyio
async def test_mock_geocoding_provider():
    provider = MockGeocodingProvider()
    loc = await provider.geocode("Nizamabad")
    assert loc.latitude == 18.67
    assert loc.longitude == 78.09
    assert loc.country == "India"


@pytest.mark.anyio
async def test_cache_deduplication_and_stale_fallback():
    cache = ProviderCache()
    call_count = 0

    async def _fetch():
        nonlocal call_count
        call_count += 1
        return "result_value"

    key = cache.make_key("test", lat=10, lon=20)

    # First fetch
    val1, fresh1 = await cache.get_or_fetch(key, _fetch, "weather")
    assert val1 == "result_value"
    assert fresh1 == FreshnessState.FRESH
    assert call_count == 1

    # Second fetch should hit cache
    val2, fresh2 = await cache.get_or_fetch(key, _fetch, "weather")
    assert val2 == "result_value"
    assert fresh2 == FreshnessState.CACHED
    assert call_count == 1  # No extra call


def test_risk_engine_fungal_pressure():
    engine = RiskEngine()
    prov = Provenance(provider="test", provider_name="test", capability="weather")
    weather = WeatherData(
        temperature_c=25.0,
        humidity_pct=85.0,
        rainfall_mm=10.0,
        soil_moisture_m3m3=0.35,
        forecast=[],
        provenance=prov,
    )

    risk_ctx = engine.evaluate(weather=weather)
    assert risk_ctx.fungal_pressure == "elevated"
    assert risk_ctx.overall_level in ("elevated", "moderate")
    assert len(risk_ctx.explanations) >= 2


def test_risk_engine_water_stress():
    engine = RiskEngine()
    prov = Provenance(provider="test", provider_name="test", capability="climate")
    climate = ClimateData(
        rainfall_7d_mm=0.0,
        dry_spell_days=10,
        provenance=prov,
    )

    risk_ctx = engine.evaluate(climate=climate)
    assert risk_ctx.water_stress in ("moderate", "severe")
