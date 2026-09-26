import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

from models.soil.inference import SoilInference
from app.schemas import ModelProvenance, RiskContextSchema, SoilAdviseRequest
from app.services.rag import rag_service

soil_inference = SoilInference()


def advise_soil_readings(
    readings: SoilAdviseRequest,
    risk_context: RiskContextSchema | None = None,
    weather_summary: str | None = None,
) -> dict:
    # 1. Preserve ML model prediction contract
    prediction = soil_inference.predict(
        n=readings.nitrogen,
        p=readings.phosphorus,
        k=readings.potassium,
        ph=readings.ph,
        moisture=readings.moisture,
    )

    category = prediction["category"]
    confidence = prediction.get("confidence")
    version = prediction["version"]
    is_synthetic = prediction["is_synthetic"]

    # 2. Query RAG for soil advisory
    crop_str = readings.crop or "General"
    query = f"Soil health N={readings.nitrogen} P={readings.phosphorus} K={readings.potassium} pH={readings.ph} moisture={readings.moisture}% for {crop_str}"
    rag_res = rag_service.generate_advisory(
        query=query,
        weather_summary=weather_summary,
        risk_summary=risk_context.water_stress if risk_context else None,
    )

    provenance = ModelProvenance(
        model_name="SoilInference-XGBoost",
        model_version=version,
        inference_mode="synthetic",
        training_data="Synthetic Soil Quality Dataset",
        field_validated=False,
        limitation="Trained on synthetic dataset. Laboratory soil testing recommended.",
    )

    return {
        "predicted_category": category,
        "confidence": confidence,
        "model_version": version,
        "is_synthetic": is_synthetic,
        "limitation": prediction["limitation"],
        "farm_id": readings.farm_id,
        "risk_context": risk_context,
        "weather_summary": weather_summary,
        "citations": rag_res["citations"],
        "model_provenance": provenance,
    }
