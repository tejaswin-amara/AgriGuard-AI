from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class DiseaseAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    crop: str
    image_path: str
    predicted_class: str
    confidence: float
    model_version: str
    is_demo: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SoilReading(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    moisture: float
    crop: Optional[str] = None
    predicted_category: str
    confidence: Optional[float] = None
    model_version: str
    is_synthetic: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdvisoryRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_type: str  # 'disease' or 'soil'
    source_id: int
    recommendation: str
    provider: str
    citations: str  # JSON string of citations
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
