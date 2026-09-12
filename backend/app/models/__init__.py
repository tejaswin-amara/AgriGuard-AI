from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class DiseaseAnalysis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    crop: str
    image_path: str
    predicted_class: str
    confidence: float
    model_version: str
    is_demo: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SoilReading(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
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
    source_type: str  # 'disease' or 'soil'
    source_id: int
    recommendation: str
    provider: str
    citations: str  # JSON string of citations
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
