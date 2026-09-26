from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Farm(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    location_query: str
    latitude: float
    longitude: float
    elevation_m: float | None = None
    timezone: str = "UTC"
    primary_crop: str = "General"
    plot_identifier: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FarmLocation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int = Field(foreign_key="farm.id", index=True)
    display_name: str
    country: str | None = None
    state: str | None = None
    district: str | None = None
    city: str | None = None
    village: str | None = None
    latitude: float
    longitude: float
    elevation_m: float | None = None
    raw_json: str | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExternalObservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int | None = Field(default=None, index=True)
    provider_id: str
    capability: str
    metric_key: str
    numeric_value: float | None = None
    string_value: str | None = None
    unit: str | None = None
    data_quality: str
    freshness: str
    observed_at: datetime | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_json: str | None = None


class WeatherSnapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int = Field(foreign_key="farm.id", index=True)
    temperature_c: float | None = None
    humidity_pct: float | None = None
    rainfall_mm: float | None = None
    wind_speed_kmh: float | None = None
    et0_mm: float | None = None
    vpd_kpa: float | None = None
    soil_temperature_c: float | None = None
    soil_moisture_m3m3: float | None = None
    gdd: float | None = None
    forecast_json: str | None = None
    provider: str
    freshness: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClimateSnapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int = Field(foreign_key="farm.id", index=True)
    period_label: str
    mean_temp_c: float | None = None
    total_precip_mm: float | None = None
    rainfall_7d_mm: float | None = None
    rainfall_14d_mm: float | None = None
    rainfall_30d_mm: float | None = None
    dry_spell_days: int | None = None
    gdd_cumulative: float | None = None
    et0_cumulative: float | None = None
    anomalies_json: str | None = None
    provider: str
    freshness: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EnvironmentSnapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int = Field(foreign_key="farm.id", index=True)
    pm25: float | None = None
    aqi_estimate: int | None = None
    elevation_m: float | None = None
    biodiversity_count: int = 0
    provider: str
    freshness: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DiseaseAnalysis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int | None = Field(default=None, index=True)
    crop: str
    image_path: str
    predicted_class: str
    confidence: float
    model_version: str
    is_demo: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SoilReading(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int | None = Field(default=None, index=True)
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    moisture: float
    crop: str | None = None
    predicted_category: str
    confidence: float | None = None
    model_version: str
    is_synthetic: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdvisoryRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    farm_id: int | None = Field(default=None, index=True)
    source_type: str  # 'disease' or 'soil' or 'general'
    source_id: int | None = None
    recommendation: str
    provider: str
    model_version: str = "v1"
    citations_json: str  # JSON string
    risk_signals_json: str | None = None  # JSON string
    limitations: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
