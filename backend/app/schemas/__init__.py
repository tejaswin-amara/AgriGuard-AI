from pydantic import BaseModel, Field


class DiseaseAnalyzeResponse(BaseModel):
    id: int
    crop: str
    predicted_class: str
    confidence: float
    model_version: str
    is_demo: bool
    limitation: str


class SoilAdviseRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, le=200)
    phosphorus: float = Field(..., ge=0, le=200)
    potassium: float = Field(..., ge=0, le=200)
    ph: float = Field(..., ge=0, le=14)
    moisture: float = Field(..., ge=0, le=100)
    crop: str | None = None


class SoilAdviseResponse(BaseModel):
    id: int
    predicted_category: str
    confidence: float | None
    model_version: str
    is_synthetic: bool
    limitation: str


class AdvisoryGenerateRequest(BaseModel):
    source_reading_type: str = Field(..., pattern="^(disease|soil)$")
    source_reading_id: int


class Citation(BaseModel):
    title: str
    organization: str
    content: str
    document_id: str


class AdvisoryGenerateResponse(BaseModel):
    id: int
    recommendation: str
    provider: str
    citations: list[Citation]
    limitation: str
