from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class DataQuality(str, Enum):
    LAB_MEASUREMENT = "LAB_MEASUREMENT"
    SENSOR_MEASUREMENT = "SENSOR_MEASUREMENT"
    OFFICIAL_OBSERVATION = "OFFICIAL_OBSERVATION"
    REMOTE_SENSING = "REMOTE_SENSING"
    WEATHER_MODEL = "WEATHER_MODEL"
    HISTORICAL_CLIMATE = "HISTORICAL_CLIMATE"
    ML_PREDICTION = "ML_PREDICTION"
    LLM_OUTPUT = "LLM_OUTPUT"
    NEWS_SOURCE = "NEWS_SOURCE"
    HEURISTIC = "HEURISTIC"


class FreshnessState(str, Enum):
    FRESH = "fresh"
    CACHED = "cached"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


class Provenance(BaseModel):
    provider: str
    provider_name: str
    capability: str
    source_url: str | None = None
    observed_at: datetime | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data_quality: DataQuality = DataQuality.WEATHER_MODEL
    freshness: FreshnessState = FreshnessState.FRESH
    attribution: str | None = None
    notes: str | None = None


class GeocodedLocation(BaseModel):
    name: str
    display_name: str
    latitude: float
    longitude: float
    elevation_m: float | None = None
    country: str | None = None
    state: str | None = None
    district: str | None = None
    city: str | None = None
    village: str | None = None
    provenance: Provenance


class ForecastDay(BaseModel):
    date: str
    min_temp_c: float | None = None
    max_temp_c: float | None = None
    precipitation_mm: float | None = None
    et0_mm: float | None = None


class WeatherData(BaseModel):
    temperature_c: float | None = None
    humidity_pct: float | None = None
    rainfall_mm: float | None = None
    wind_speed_kmh: float | None = None
    solar_radiation_mj: float | None = None
    et0_mm: float | None = None
    vpd_kpa: float | None = None
    soil_temperature_c: float | None = None
    soil_moisture_m3m3: float | None = None
    gdd: float | None = None
    forecast: list[ForecastDay] = Field(default_factory=list)
    provenance: Provenance


class ClimateData(BaseModel):
    period_label: str = "Historical Baseline"
    mean_temp_c: float | None = None
    min_temp_c: float | None = None
    max_temp_c: float | None = None
    total_precipitation_mm: float | None = None
    rainfall_7d_mm: float | None = None
    rainfall_14d_mm: float | None = None
    rainfall_30d_mm: float | None = None
    dry_spell_days: int | None = None
    gdd_cumulative: float | None = None
    et0_cumulative: float | None = None
    anomalies: dict[str, float] = Field(default_factory=dict)
    provenance: Provenance


class AirQualityData(BaseModel):
    pm25: float | None = None
    pm10: float | None = None
    no2: float | None = None
    o3: float | None = None
    aqi_estimate: int | None = None
    provenance: Provenance


class ElevationData(BaseModel):
    elevation_m: float
    provenance: Provenance


class BiodiversityObservation(BaseModel):
    species_name: str
    common_name: str | None = None
    category: str = "general"
    observation_count: int = 1
    last_observed_at: str | None = None
    dataset: str | None = None


class BiodiversityData(BaseModel):
    total_observations: int = 0
    observations: list[BiodiversityObservation] = Field(default_factory=list)
    provenance: Provenance


class NewsArticle(BaseModel):
    title: str
    summary: str | None = None
    source: str
    url: str
    published_at: str | None = None
    category: str = "agriculture"


class NewsData(BaseModel):
    articles: list[NewsArticle] = Field(default_factory=list)
    provenance: Provenance


class ProviderStatusInfo(BaseModel):
    provider_id: str
    name: str
    category: str
    is_required: bool
    enabled: bool
    status: str
    latency_ms: float | None = None
    last_success: datetime | None = None
    last_failure: datetime | None = None
    error_message: str | None = None
