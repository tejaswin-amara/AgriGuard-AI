import time
from datetime import datetime, timezone
from app.services.external.base import (
    AirQualityProvider,
    BiodiversityProvider,
    ClimateProvider,
    ElevationProvider,
    GeocodingProvider,
    NewsProvider,
    WeatherProvider,
)
from app.services.external.types import (
    AirQualityData,
    BiodiversityData,
    BiodiversityObservation,
    ClimateData,
    DataQuality,
    ElevationData,
    ForecastDay,
    FreshnessState,
    GeocodedLocation,
    NewsArticle,
    NewsData,
    Provenance,
    ProviderStatusInfo,
    WeatherData,
)


class MockWeatherProvider(WeatherProvider):
    provider_id = "mock_weather"
    provider_name = "Mock Weather Provider (Test)"
    is_required = True

    async def get_weather(self, lat: float, lon: float) -> WeatherData:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.WEATHER_MODEL,
            freshness=FreshnessState.FRESH,
        )
        return WeatherData(
            temperature_c=28.5,
            humidity_pct=82.0,
            rainfall_mm=12.5,
            wind_speed_kmh=10.0,
            solar_radiation_mj=18.5,
            et0_mm=4.2,
            vpd_kpa=0.72,
            soil_temperature_c=24.0,
            soil_moisture_m3m3=0.32,
            gdd=14.5,
            forecast=[
                ForecastDay(date="2026-09-27", min_temp_c=22.0, max_temp_c=31.0, precipitation_mm=2.0, et0_mm=4.1),
                ForecastDay(date="2026-09-28", min_temp_c=21.5, max_temp_c=30.5, precipitation_mm=0.0, et0_mm=4.3),
            ],
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )


class MockClimateProvider(ClimateProvider):
    provider_id = "mock_climate"
    provider_name = "Mock Climate Provider (Test)"
    is_required = True

    async def get_climate(self, lat: float, lon: float) -> ClimateData:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.HISTORICAL_CLIMATE,
            freshness=FreshnessState.FRESH,
        )
        return ClimateData(
            period_label="Mock 30-Day Climate Baseline",
            mean_temp_c=27.2,
            min_temp_c=20.1,
            max_temp_c=33.5,
            total_precipitation_mm=112.0,
            rainfall_7d_mm=28.0,
            rainfall_14d_mm=54.0,
            rainfall_30d_mm=112.0,
            dry_spell_days=2,
            gdd_cumulative=420.0,
            et0_cumulative=125.0,
            anomalies={"rainfall_30d_vs_normal": 12.0},
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )


class MockGeocodingProvider(GeocodingProvider):
    provider_id = "mock_geocoding"
    provider_name = "Mock Geocoder (Test)"
    is_required = True

    async def geocode(self, query: str) -> GeocodedLocation:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.OFFICIAL_OBSERVATION,
            freshness=FreshnessState.FRESH,
        )
        return GeocodedLocation(
            name=query,
            display_name=f"{query}, Telangana, India",
            latitude=18.67,
            longitude=78.09,
            country="India",
            state="Telangana",
            district="Nizamabad",
            city="Nizamabad",
            provenance=provenance,
        )

    async def reverse_geocode(self, lat: float, lon: float) -> GeocodedLocation:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.OFFICIAL_OBSERVATION,
            freshness=FreshnessState.FRESH,
        )
        return GeocodedLocation(
            name=f"Farm Location ({lat:.2f}, {lon:.2f})",
            display_name=f"Farm Plot at {lat:.4f}, {lon:.4f}, Telangana, India",
            latitude=lat,
            longitude=lon,
            country="India",
            state="Telangana",
            district="Nizamabad",
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )


class MockAirQualityProvider(AirQualityProvider):
    provider_id = "mock_openaq"
    provider_name = "Mock Air Quality Provider"
    is_required = False

    async def get_air_quality(self, lat: float, lon: float) -> AirQualityData:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.SENSOR_MEASUREMENT,
            freshness=FreshnessState.FRESH,
        )
        return AirQualityData(
            pm25=22.4,
            pm10=45.1,
            no2=12.3,
            o3=34.1,
            aqi_estimate=72,
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )


class MockElevationProvider(ElevationProvider):
    provider_id = "mock_elevation"
    provider_name = "Mock Elevation Provider"
    is_required = False

    async def get_elevation(self, lat: float, lon: float) -> ElevationData:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.REMOTE_SENSING,
            freshness=FreshnessState.FRESH,
        )
        return ElevationData(elevation_m=395.0, provenance=provenance)

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )


class MockBiodiversityProvider(BiodiversityProvider):
    provider_id = "mock_gbif"
    provider_name = "Mock GBIF Provider"
    is_required = False

    async def get_biodiversity(self, lat: float, lon: float) -> BiodiversityData:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.OFFICIAL_OBSERVATION,
            freshness=FreshnessState.FRESH,
        )
        return BiodiversityData(
            total_observations=15,
            observations=[
                BiodiversityObservation(
                    species_name="Apis cerana",
                    common_name="Asiatic Honeybee",
                    category="pollinator",
                    observation_count=8,
                    last_observed_at="2026-08-15",
                ),
                BiodiversityObservation(
                    species_name="Coccinella septempunctata",
                    common_name="Seven-spot Ladybird",
                    category="beneficial predator",
                    observation_count=7,
                    last_observed_at="2026-08-20",
                ),
            ],
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )


class MockNewsProvider(NewsProvider):
    provider_id = "mock_news"
    provider_name = "Mock Agriculture News Provider"
    is_required = False

    async def get_news(self, query: str = "agriculture") -> NewsData:
        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            data_quality=DataQuality.NEWS_SOURCE,
            freshness=FreshnessState.FRESH,
        )
        return NewsData(
            articles=[
                NewsArticle(
                    title="Mock Advisory: Monsoon Soil Health and Pest Monitoring",
                    summary="Monsoon advisory for smallholder farmers on soil moisture retention.",
                    source="Mock AgroMet News",
                    url="https://agri.example.org/news/1",
                    published_at="2026-09-25",
                )
            ],
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        return ProviderStatusInfo(
            provider_id=self.provider_id,
            name=self.provider_name,
            category=self.category,
            is_required=self.is_required,
            enabled=True,
            status="healthy",
            latency_ms=1.0,
            last_success=datetime.now(timezone.utc),
        )
