import json

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models import AdvisoryRecord, DiseaseAnalysis, Farm, SoilReading
from app.schemas import (
    AdvisoryDetailResponse,
    AdvisoryGenerateRequest,
    AdvisoryGenerateResponse,
    Citation,
)
from app.services.farm_context import farm_context_service
from app.services.rag import rag_service

router = APIRouter(prefix="/advisory", tags=["Advisory"])


@router.post(
    "/generate",
    response_model=AdvisoryGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Grounded Agricultural Advisory",
)
async def generate_advisory(
    req: AdvisoryGenerateRequest,
    session: Session = Depends(get_session),
):
    query = req.custom_query or "General crop health management"
    risk_ctx = None
    weather_summary = None

    # Retrieve source reading or farm context
    if req.source_reading_type == "disease" and req.source_reading_id:
        disease = session.get(DiseaseAnalysis, req.source_reading_id)
        if disease:
            query = f"{disease.crop} {disease.predicted_class} leaf disease treatment and management"
            if disease.farm_id:
                req.farm_id = disease.farm_id

    elif req.source_reading_type == "soil" and req.source_reading_id:
        soil = session.get(SoilReading, req.source_reading_id)
        if soil:
            crop_str = soil.crop or "crop"
            query = f"Soil amendment for {soil.predicted_category} category N={soil.nitrogen} P={soil.phosphorus} K={soil.potassium} pH={soil.ph} for {crop_str}"
            if soil.farm_id:
                req.farm_id = soil.farm_id

    if req.farm_id:
        farm = session.get(Farm, req.farm_id)
        if farm:
            fctx = await farm_context_service.get_farm_context(session, farm)
            risk_ctx = fctx.risk_context
            weather_summary = f"Temp: {fctx.weather.temperature_c}°C, Humidity: {fctx.weather.humidity_pct}%, Precip: {fctx.weather.rainfall_mm}mm"

    # Generate RAG & LLM grounded response
    rag_res = rag_service.generate_advisory(
        query=query,
        weather_summary=weather_summary,
        risk_summary=risk_ctx.overall_level if risk_ctx else None,
    )

    citations_json = json.dumps([c.model_dump() for c in rag_res["citations"]])
    risk_json = json.dumps(risk_ctx.model_dump()) if risk_ctx else None

    record = AdvisoryRecord(
        farm_id=req.farm_id,
        source_type=req.source_reading_type,
        source_id=req.source_reading_id,
        recommendation=rag_res["recommendation"],
        provider=rag_res["provider"],
        citations_json=citations_json,
        risk_signals_json=risk_json,
        limitations=rag_res["limitation"],
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return AdvisoryGenerateResponse(
        id=record.id,
        recommendation=record.recommendation,
        provider=record.provider,
        citations=rag_res["citations"],
        limitation=record.limitations,
        risk_signals=risk_ctx,
        created_at=record.created_at,
    )


@router.get(
    "s", response_model=list[AdvisoryDetailResponse], summary="List Advisory History"
)
def list_advisories(
    farm_id: int | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    stmt = select(AdvisoryRecord)
    if farm_id:
        stmt = stmt.where(AdvisoryRecord.farm_id == farm_id)
    stmt = stmt.order_by(AdvisoryRecord.created_at.desc()).limit(limit)
    records = session.exec(stmt).all()

    out = []
    for r in records:
        citations = [Citation(**c) for c in json.loads(r.citations_json or "[]")]
        risk_signals = json.loads(r.risk_signals_json) if r.risk_signals_json else None
        out.append(
            AdvisoryDetailResponse(
                id=r.id,
                farm_id=r.farm_id,
                source_type=r.source_type,
                source_id=r.source_id,
                recommendation=r.recommendation,
                provider=r.provider,
                model_version=r.model_version,
                citations=citations,
                risk_signals=risk_signals,
                limitations=r.limitations,
                created_at=r.created_at,
            )
        )
    return out


@router.get(
    "s/{advisory_id}",
    response_model=AdvisoryDetailResponse,
    summary="Get Advisory details by ID",
)
def get_advisory(advisory_id: int, session: Session = Depends(get_session)):
    r = session.get(AdvisoryRecord, advisory_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Advisory {advisory_id} not found")

    citations = [Citation(**c) for c in json.loads(r.citations_json or "[]")]
    risk_signals = json.loads(r.risk_signals_json) if r.risk_signals_json else None

    return AdvisoryDetailResponse(
        id=r.id,
        farm_id=r.farm_id,
        source_type=r.source_type,
        source_id=r.source_id,
        recommendation=r.recommendation,
        provider=r.provider,
        model_version=r.model_version,
        citations=citations,
        risk_signals=risk_signals,
        limitations=r.limitations,
        created_at=r.created_at,
    )
