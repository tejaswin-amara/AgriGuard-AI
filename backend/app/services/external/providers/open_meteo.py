import math
import time
from datetime import datetime, timezone

from app.services.external.base import WeatherProvider
from app.services.external.errors import ProviderResponseError
from app.services.external.transport import transport
from app.services.external.types import (
    DataQuality,
    ForecastDay,
    FreshnessState,
    Provenance,
    ProviderStatusInfo,
    WeatherData,
)


class OpenMeteoWeatherProvider(WeatherProvider):
    provider_id = "open_meteo"
    provider_name = "Open-Meteo Weather API"
    is_required = True
    base_url = "https://api.open-meteo.com/v1/forecast"

    async def get_weather(self, lat: float, lon: float) -> WeatherData:
        params = {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,soil_temperature_0cm,soil_moisture_0_to_1cm",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
            "timezone": "auto",
        }

        data = await transport.get_json(self.provider_id, self.base_url, params=params)
        if not isinstance(data, dict):
            raise ProviderResponseError(
                self.provider_id, "Expected JSON object from Open-Meteo"
            )

        current = data.get("current", {})
        daily = data.get("daily", {})

        temp_c = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        precip = current.get("precipitation")
        wind = current.get("wind_speed_10m")
        soil_temp = current.get("soil_temperature_0cm")
        soil_moisture = current.get("soil_moisture_0_to_1cm")

        # Compute Vapor Pressure Deficit (VPD) if temp & humidity exist
        vpd_kpa = None
        if temp_c is not None and humidity is not None:
            es = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
            ea = es * (humidity / 100.0)
            vpd_kpa = round(max(0.0, es - ea), 3)

        forecast_days: list[ForecastDay] = []
        daily_times = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        precip_sums = daily.get("precipitation_sum", [])
        et0_vals = daily.get("et0_fao_evapotranspiration", [])

        gdd_val = None
        et0_val = None

        for idx, date_str in enumerate(daily_times):
            tmax = max_temps[idx] if idx < len(max_temps) else None
            tmin = min_temps[idx] if idx < len(min_temps) else None
            psum = precip_sums[idx] if idx < len(precip_sums) else None
            et0 = et0_vals[idx] if idx < len(et0_vals) else None

            if idx == 0:
                et0_val = et0
                if tmax is not None and tmin is not None:
                    tavg = (tmax + tmin) / 2.0
                    gdd_val = round(max(0.0, tavg - 10.0), 2)

            forecast_days.append(
                ForecastDay(
                    date=date_str,
                    min_temp_c=tmin,
                    max_temp_c=tmax,
                    precipitation_mm=psum,
                    et0_mm=et0,
                )
            )

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://open-meteo.com/",
            observed_at=datetime.now(timezone.utc),
            data_quality=DataQuality.WEATHER_MODEL,
            freshness=FreshnessState.FRESH,
            attribution="Weather data by Open-Meteo.com",
        )

        return WeatherData(
            temperature_c=temp_c,
            humidity_pct=humidity,
            rainfall_mm=precip,
            wind_speed_kmh=wind,
            solar_radiation_mj=None,
            et0_mm=et0_val,
            vpd_kpa=vpd_kpa,
            soil_temperature_c=soil_temp,
            soil_moisture_m3m3=soil_moisture,
            gdd=gdd_val,
            forecast=forecast_days,
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        start = time.perf_counter()
        try:
            await transport.get_json(
                self.provider_id,
                self.base_url,
                params={"latitude": 0, "longitude": 0, "current": "temperature_2m"},
            )
            latency = (time.perf_counter() - start) * 1000
            return ProviderStatusInfo(
                provider_id=self.provider_id,
                name=self.provider_name,
                category=self.category,
                is_required=self.is_required,
                enabled=True,
                status="healthy",
                latency_ms=round(latency, 1),
                last_success=datetime.now(timezone.utc),
            )
        except Exception as e:
            return ProviderStatusInfo(
                provider_id=self.provider_id,
                name=self.provider_name,
                category=self.category,
                is_required=self.is_required,
                enabled=True,
                status="unavailable",
                error_message=str(e),
                last_failure=datetime.now(timezone.utc),
            )
