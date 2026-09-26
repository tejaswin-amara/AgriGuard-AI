from fastapi import APIRouter, HTTPException, Query

from app.services.external.providers.open_topo_data import OpenTopoDataElevationProvider
from app.services.external.providers.openaq import OpenAQAirQualityProvider
from app.services.external.types import AirQualityData, ElevationData

router = APIRouter(prefix="/environment", tags=["Environment"])
aq_provider = OpenAQAirQualityProvider()
elev_provider = OpenTopoDataElevationProvider()


@router.get(
    "/air-quality",
    response_model=AirQualityData,
    summary="Get Environmental Air Quality Data",
)
async def get_air_quality(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    try:
        return await aq_provider.get_air_quality(lat, lon)
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Air quality provider error: {e!s}"
        )


@router.get("/elevation", response_model=ElevationData, summary="Get Terrain Elevation")
async def get_elevation(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    try:
        return await elev_provider.get_elevation(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Elevation provider error: {e!s}")
