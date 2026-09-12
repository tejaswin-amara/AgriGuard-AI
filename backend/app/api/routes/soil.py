from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import SoilReading
from app.schemas import SoilAdviseRequest, SoilAdviseResponse
from app.services.soil import advise_soil_readings

router = APIRouter(prefix="/soil", tags=["soil"])


@router.post("/advise", response_model=SoilAdviseResponse)
def advise_soil(request: SoilAdviseRequest, session: SessionDep):
    """
    Get soil health advisory based on readings.
    """
    result = advise_soil_readings(request)

    record = SoilReading(
        nitrogen=request.nitrogen,
        phosphorus=request.phosphorus,
        potassium=request.potassium,
        ph=request.ph,
        moisture=request.moisture,
        crop=request.crop,
        predicted_category=result["category"],
        confidence=result["confidence"],
        model_version=result["version"],
        is_synthetic=result["is_synthetic"],
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return SoilAdviseResponse(
        id=record.id,
        predicted_category=record.predicted_category,
        confidence=record.confidence,
        model_version=record.model_version,
        is_synthetic=record.is_synthetic,
        limitation=result["limitation"],
    )
