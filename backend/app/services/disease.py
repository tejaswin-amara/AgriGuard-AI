import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

from models.disease.inference import DiseaseInference
from app.schemas import Citation, ModelProvenance, RiskContextSchema
from app.services.rag import rag_service

disease_inference = DiseaseInference()


def analyze_disease_image(
    image_bytes: bytes,
    crop: str = "General",
    risk_context: RiskContextSchema | None = None,
    weather_summary: str | None = None,
) -> dict:
    # 1. Preserve ML model prediction contract
    prediction = disease_inference.predict(image_bytes)

    predicted_class = prediction["class"]
    confidence = prediction["confidence"]
    version = prediction["version"]
    is_demo = prediction["is_demo"]

    # 2. Query RAG for disease management citations
    query = f"{crop} {predicted_class} leaf disease management guidelines"
    rag_res = rag_service.generate_advisory(
        query=query,
        weather_summary=weather_summary,
        risk_summary=risk_context.fungal_pressure if risk_context else None,
    )

    provenance = ModelProvenance(
        model_name="DiseaseInference-MobileNet",
        model_version=version,
        inference_mode="demo" if is_demo else "production",
        training_data="PlantVillage Public Leaf Dataset",
        field_validated=False,
        limitation="Demo model output. Not a validated field diagnosis.",
    )

    return {
        "crop": crop,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "model_version": version,
        "is_demo": is_demo,
        "limitation": prediction["limitation"],
        "risk_context": risk_context,
        "weather_summary": weather_summary,
        "citations": rag_res["citations"],
        "model_provenance": provenance,
    }
