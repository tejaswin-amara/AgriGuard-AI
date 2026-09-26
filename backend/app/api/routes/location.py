from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.external.providers.nominatim import NominatimGeocodingProvider
from app.services.external.types import GeocodedLocation

router = APIRouter(prefix="/location", tags=["Location"])
geocoder = NominatimGeocodingProvider()


class GeocodeRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=200)


@router.post(
    "/geocode", response_model=GeocodedLocation, summary="Forward Geocode Location Name"
)
async def geocode_location(req: GeocodeRequest):
    try:
        return await geocoder.geocode(req.query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/reverse", response_model=GeocodedLocation, summary="Reverse Geocode Coordinates"
)
async def reverse_geocode_location(lat: float, lon: float):
    try:
        return await geocoder.reverse_geocode(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
