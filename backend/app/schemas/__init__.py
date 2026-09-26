from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.services.external.types import (
    AirQualityData,
    BiodiversityData,
    ClimateData,
    ElevationData,
    GeocodedLocation,
    NewsArticle,
    NewsData,
    ProviderStatusInfo,
    WeatherData,
)


class Citation(BaseModel):
    title: str
    organization: str
    content: str
    document_id: str
    url: str | None = None
    provider: str | None = None
    source_type: str | None = "knowledge_document"  # knowledge_document, external_observation, historical_climate, model_output, news
    data_quality: str | None = "modelled"


class ModelProvenance(BaseModel):
    model_name: str
    model_version: str
    inference_mode: str = "demo"  # demo, production, synthetic
    training_data: str = "synthetic"
    field_validated: bool = False
    limitation: str


class RiskSignal(BaseModel):
    name: str
    level: str  # low, moderate, elevated, severe
    score: float  # 0.0 - 1.0 (heuristic indicator score)
    explanation: str


class RiskContextSchema(BaseModel):
    fungal_pressure: str = "low"
    water_stress: str = "optimal"
    heat_stress: str = "none"
    overall_level: str = "low"
    signals: list[RiskSignal] = Field(default_factory=list)
    explanations: list[str] = Field(default_factory=list)


class FarmCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    location_query: str = Field(..., min_length=2, max_length=200)
    primary_crop: str = "General"
    plot_identifier: str | None = None


class FarmResponse(BaseModel):
    id: int
    name: str
    location_query: str
    latitude: float
    longitude: float
    elevation_m: float | None = None
    timezone: str
    primary_crop: str
    plot_identifier: str | None = None
    created_at: datetime
    updated_at: datetime


class FarmContextResponse(BaseModel):
    farm: FarmResponse
    location: GeocodedLocation
    weather: WeatherData
    climate: ClimateData
    air_quality: AirQualityData | None = None
    elevation: ElevationData | None = None
    biodiversity: BiodiversityData | None = None
    news: NewsData | None = None
    risk_context: RiskContextSchema
    provider_status: list[ProviderStatusInfo] = Field(default_factory=list)
    freshness: dict[str, str] = Field(default_factory=dict)


class DiseaseAnalyzeResponse(BaseModel):
    id: int
    crop: str
    predicted_class: str
    confidence: float
    model_version: str
    is_demo: bool
    limitation: str
    farm_id: int | None = None
    risk_context: RiskContextSchema | None = None
    weather_summary: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    model_provenance: ModelProvenance


class SoilAdviseRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=200)
    phosphorus: float = Field(..., ge=0, le=200)
    potassium: float = Field(..., ge=0, le=200)
    ph: float = Field(..., ge=0, le=14)
    moisture: float = Field(..., ge=0, le=100)
    crop: str | None = None
    farm_id: int | None = None


class SoilAdviseResponse(BaseModel):
    id: int
    predicted_category: str
    confidence: float | None
    model_version: str
    is_synthetic: bool
    limitation: str
    farm_id: int | None = None
    risk_context: RiskContextSchema | None = None
    weather_summary: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    model_provenance: ModelProvenance


class AdvisoryGenerateRequest(BaseModel):
    source_reading_type: str = Field(..., pattern="^(disease|soil|general)$")
    source_reading_id: int | None = None
    farm_id: int | None = None
    custom_query: str | None = None


class AdvisoryGenerateResponse(BaseModel):
    id: int
    recommendation: str
    provider: str
    citations: list[Citation]
    limitation: str
    risk_signals: RiskContextSchema | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdvisoryDetailResponse(BaseModel):
    id: int
    farm_id: int | None = None
    source_type: str
    source_id: int | None = None
    recommendation: str
    provider: str
    model_version: str
    citations: list[Citation]
    risk_signals: RiskContextSchema | None = None
    limitations: str
    created_at: datetime
