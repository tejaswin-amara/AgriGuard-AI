from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.deps import get_session
from app.models import Farm, SoilReading
from app.schemas import SoilAdviseRequest, SoilAdviseResponse
from app.services.farm_context import farm_context_service
from app.services.soil import advise_soil_readings

router = APIRouter(prefix="/soil", tags=["Soil"])


@router.post(
    "/advise",
    response_model=SoilAdviseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze Soil Health Parameters with Environmental Context",
)
async def advise_soil(readings: SoilAdviseRequest, session: Session = Depends(get_session)):
    # 1. Fetch farm context if farm_id provided
    risk_ctx = None
    weather_summary = None
    if readings.farm_id:
        farm = session.get(Farm, readings.farm_id)
        if farm:
            fctx = await farm_context_service.get_farm_context(session, farm)
            risk_ctx = fctx.risk_context
            weather_summary = f"Temp: {fctx.weather.temperature_c}°C, Humidity: {fctx.weather.humidity_pct}%, Soil Moisture: {fctx.weather.soil_moisture_m3m3}"

    # 2. Perform ML soil analysis
    result = advise_soil_readings(
        readings=readings,
        risk_context=risk_ctx,
        weather_summary=weather_summary,
    )

    # 3. Persist soil reading record
    record = SoilReading(
        farm_id=readings.farm_id,
        nitrogen=readings.nitrogen,
        phosphorus=readings.phosphorus,
        potassium=readings.potassium,
        ph=readings.ph,
        moisture=readings.moisture,
        crop=readings.crop,
        predicted_category=result["predicted_category"],
        confidence=result["confidence"],
        model_version=result["model_version"],
        is_synthetic=result["is_synthetic"],
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return SoilAdviseResponse(
        id=record.id,
        predicted_category=result["predicted_category"],
        confidence=result["confidence"],
        model_version=result["model_version"],
        is_synthetic=result["is_synthetic"],
        limitation=result["limitation"],
        farm_id=readings.farm_id,
        risk_context=risk_ctx,
        weather_summary=weather_summary,
        citations=result["citations"],
        model_provenance=result["model_provenance"],
    )
