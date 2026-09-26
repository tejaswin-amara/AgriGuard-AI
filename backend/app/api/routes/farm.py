from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models import Farm, FarmLocation
from app.schemas import FarmContextResponse, FarmCreate, FarmResponse
from app.services.farm_context import farm_context_service

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("", response_model=FarmResponse, status_code=status.HTTP_201_CREATED, summary="Create a new Farm")
async def create_farm(farm_in: FarmCreate, session: Session = Depends(get_session)):
    # Resolve geocoding to get coordinates
    try:
        location = await farm_context_service.geocoding_provider.geocode(farm_in.location_query)
        lat, lon = location.latitude, location.longitude
        elevation = location.elevation_m
    except Exception as e:
        # Fallback default coordinates if geocoder times out or fails
        lat, lon = 18.67, 78.09
        elevation = 395.0

    farm = Farm(
        name=farm_in.name,
        location_query=farm_in.location_query,
        latitude=lat,
        longitude=lon,
        elevation_m=elevation,
        primary_crop=farm_in.primary_crop,
        plot_identifier=farm_in.plot_identifier,
    )
    session.add(farm)
    session.commit()
    session.refresh(farm)

    # Persist resolved location record
    farm_loc = FarmLocation(
        farm_id=farm.id,
        display_name=location.display_name if 'location' in locals() else farm_in.location_query,
        latitude=lat,
        longitude=lon,
        elevation_m=elevation,
    )
    session.add(farm_loc)
    session.commit()

    return farm


@router.get("", response_model=list[FarmResponse], summary="List all Farms")
def list_farms(session: Session = Depends(get_session)):
    farms = session.exec(select(Farm)).all()
    return farms


@router.get("/{farm_id}", response_model=FarmResponse, summary="Get Farm details")
def get_farm(farm_id: int, session: Session = Depends(get_session)):
    farm = session.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm {farm_id} not found")
    return farm


@router.get("/{farm_id}/context", response_model=FarmContextResponse, summary="Get aggregated Farm Context")
async def get_farm_context(farm_id: int, session: Session = Depends(get_session)):
    farm = session.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm {farm_id} not found")

    return await farm_context_service.get_farm_context(session, farm)
