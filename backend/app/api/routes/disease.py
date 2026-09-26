import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlmodel import Session

from app.api.deps import get_session
from app.models import DiseaseAnalysis, Farm
from app.schemas import DiseaseAnalyzeResponse
from app.services.disease import analyze_disease_image
from app.services.farm_context import farm_context_service

router = APIRouter(prefix="/disease", tags=["Disease"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/pjpeg"}


@router.post(
    "/analyze",
    response_model=DiseaseAnalyzeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze Leaf Image for Crop Disease with Environmental Context",
)
async def analyze_disease(
    file: UploadFile = File(None),
    image: UploadFile = File(None),
    crop: str = Form("General"),
    farm_id: int | None = Form(None),
    session: Session = Depends(get_session),
):
    upload_file = file or image
    if not upload_file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing image file. Please upload an image file under parameter 'file' or 'image'.",
        )

    if (
        not upload_file.content_type
        or upload_file.content_type.lower() not in ALLOWED_MIME_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Supported formats are JPEG, PNG, and WebP.",
        )

    # Read image file bytes with 10MB upload limit
    image_bytes = await upload_file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum 10MB limit.",
        )

    # 1. Fetch farm context if farm_id provided
    risk_ctx = None
    weather_summary = None
    if farm_id:
        farm = session.get(Farm, farm_id)
        if farm:
            fctx = await farm_context_service.get_farm_context(session, farm)
            risk_ctx = fctx.risk_context
            if fctx.weather:
                weather_summary = f"Temp: {fctx.weather.temperature_c}°C, Humidity: {fctx.weather.humidity_pct}%, Rainfall: {fctx.weather.rainfall_mm}mm"

    # 2. Perform ML disease analysis
    try:
        analysis_result = analyze_disease_image(
            image_bytes=image_bytes,
            crop=crop,
            risk_context=risk_ctx,
            weather_summary=weather_summary,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # 3. Generate server-side secure object key
    raw_ext = Path(upload_file.filename or "image.jpg").suffix.lower()
    ext = raw_ext if raw_ext in (".jpg", ".jpeg", ".png", ".webp") else ".jpg"
    secure_filename = f"leaf_{uuid.uuid4().hex}{ext}"

    # 4. Persist analysis record
    record = DiseaseAnalysis(
        farm_id=farm_id,
        crop=crop,
        image_path=f"uploads/{secure_filename}",
        predicted_class=analysis_result["predicted_class"],
        confidence=analysis_result["confidence"],
        model_version=analysis_result["model_version"],
        is_demo=analysis_result["is_demo"],
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return DiseaseAnalyzeResponse(
        id=record.id,
        crop=crop,
        predicted_class=analysis_result["predicted_class"],
        confidence=analysis_result["confidence"],
        model_version=analysis_result["model_version"],
        is_demo=analysis_result["is_demo"],
        limitation=analysis_result["limitation"],
        farm_id=farm_id,
        risk_context=analysis_result["risk_context"],
        weather_summary=weather_summary,
        citations=analysis_result["citations"],
        model_provenance=analysis_result["model_provenance"],
    )
