from fastapi import APIRouter, HTTPException, Query
from app.services.external.providers.nasa_power import NASAPowerClimateProvider
from app.services.external.providers.open_meteo import OpenMeteoWeatherProvider
from app.services.external.types import ClimateData, WeatherData

router = APIRouter(tags=["Weather & Climate"])
weather_provider = OpenMeteoWeatherProvider()
climate_provider = NASAPowerClimateProvider()


@router.get("/weather", response_model=WeatherData, summary="Get Live Weather & Short-term Forecast")
async def get_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    try:
        return await weather_provider.get_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather provider error: {str(e)}")


@router.get("/climate", response_model=ClimateData, summary="Get Historical Agroclimate Baseline")
async def get_climate(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    try:
        return await climate_provider.get_climate(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Climate provider error: {str(e)}")
