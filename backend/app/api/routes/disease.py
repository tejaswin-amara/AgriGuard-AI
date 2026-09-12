from fastapi import APIRouter, File, UploadFile

from app.api.deps import SessionDep
from app.models import DiseaseAnalysis
from app.schemas import DiseaseAnalyzeResponse
from app.services.disease import analyze_disease_image

router = APIRouter(prefix="/disease", tags=["disease"])


@router.post("/analyze", response_model=DiseaseAnalyzeResponse)
async def analyze_disease(
    crop: str, session: SessionDep, image: UploadFile = File(...)
):
    """
    Analyze a crop leaf image for disease.
    """
    image_bytes = await image.read()
    result = analyze_disease_image(image_bytes)

    # Save to db
    record = DiseaseAnalysis(
        crop=crop,
        image_path=image.filename,
        predicted_class=result["class"],
        confidence=result["confidence"],
        model_version=result["version"],
        is_demo=result["is_demo"],
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return DiseaseAnalyzeResponse(
        id=record.id,
        crop=record.crop,
        predicted_class=record.predicted_class,
        confidence=record.confidence,
        model_version=record.model_version,
        is_demo=record.is_demo,
        limitation=result["limitation"],
    )
