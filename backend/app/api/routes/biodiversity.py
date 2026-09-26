from fastapi import APIRouter, Query
from app.services.external.providers.gbif import GBIFBiodiversityProvider
from app.services.external.types import BiodiversityData

router = APIRouter(prefix="/biodiversity", tags=["Biodiversity"])
bio_provider = GBIFBiodiversityProvider()


@router.get("", response_model=BiodiversityData, summary="Get Ecological & Biodiversity Observations")
async def get_biodiversity(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    return await bio_provider.get_biodiversity(lat, lon)
