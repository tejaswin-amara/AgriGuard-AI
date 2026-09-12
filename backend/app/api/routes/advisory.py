import json

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models import AdvisoryRecord, DiseaseAnalysis, SoilReading
from app.schemas import AdvisoryGenerateRequest, AdvisoryGenerateResponse
from app.services.rag import RAGService

router = APIRouter(prefix="/advisory", tags=["advisory"])
rag_service = RAGService()


@router.post("/generate", response_model=AdvisoryGenerateResponse)
def generate_advisory(request: AdvisoryGenerateRequest, session: SessionDep):
    """
    Generate grounded advisory.
    """
    query = ""
    if request.source_reading_type == "disease":
        record = session.get(DiseaseAnalysis, request.source_reading_id)
        if not record:
            raise HTTPException(status_code=404, detail="Disease record not found")
        query = f"Management of {record.predicted_class} in {record.crop}"
    else:
        record = session.get(SoilReading, request.source_reading_id)
        if not record:
            raise HTTPException(status_code=404, detail="Soil record not found")
        query = f"Soil management for {record.predicted_category} with pH {record.ph} and moisture {record.moisture}"

    rag_result = rag_service.generate_advisory(query)

    advisory_record = AdvisoryRecord(
        source_type=request.source_reading_type,
        source_id=request.source_reading_id,
        recommendation=rag_result["recommendation"],
        provider=rag_result["provider"],
        citations=json.dumps([c.model_dump() for c in rag_result["citations"]]),
    )
    session.add(advisory_record)
    session.commit()
    session.refresh(advisory_record)

    return AdvisoryGenerateResponse(
        id=advisory_record.id,
        recommendation=advisory_record.recommendation,
        provider=advisory_record.provider,
        citations=rag_result["citations"],
        limitation="Demo advisory generated based on prototype rules and synthetic data.",
    )
