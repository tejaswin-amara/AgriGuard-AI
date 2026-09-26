import time
from datetime import datetime, timedelta, timezone

from app.services.external.base import ClimateProvider
from app.services.external.errors import ProviderResponseError
from app.services.external.transport import transport
from app.services.external.types import (
    ClimateData,
    DataQuality,
    FreshnessState,
    Provenance,
    ProviderStatusInfo,
)


class NASAPowerClimateProvider(ClimateProvider):
    provider_id = "nasa_power"
    provider_name = "NASA POWER Agroclimate API"
    is_required = True
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    async def get_climate(self, lat: float, lon: float) -> ClimateData:
        end_dt = datetime.now(timezone.utc) - timedelta(days=2)
        start_dt = end_dt - timedelta(days=30)

        start_str = start_dt.strftime("%Y%m%d")
        end_str = end_dt.strftime("%Y%m%d")

        params = {
            "parameters": "T2M,T2M_MIN,T2M_MAX,PRECTOTCORR",
            "community": "AG",
            "longitude": round(lon, 4),
            "latitude": round(lat, 4),
            "start": start_str,
            "end": end_str,
            "format": "JSON",
        }

        data = await transport.get_json(self.provider_id, self.base_url, params=params)
        if not isinstance(data, dict) or "properties" not in data:
            raise ProviderResponseError(self.provider_id, "Expected NASA POWER properties structure")

        parameter_data = data.get("properties", {}).get("parameter", {})
        t2m_dict = parameter_data.get("T2M", {})
        t2m_min_dict = parameter_data.get("T2M_MIN", {})
        t2m_max_dict = parameter_data.get("T2M_MAX", {})
        precip_dict = parameter_data.get("PRECTOTCORR", {})

        dates_sorted = sorted(t2m_dict.keys())
        if not dates_sorted:
            raise ProviderResponseError(self.provider_id, "No climate data points returned from NASA POWER")

        temps = [t2m_dict[d] for d in dates_sorted if t2m_dict[d] != -999]
        precips = [precip_dict.get(d, 0) for d in dates_sorted if precip_dict.get(d, -999) != -999]

        mean_temp = round(sum(temps) / len(temps), 2) if temps else None
        min_temp = round(min(temps), 2) if temps else None
        max_temp = round(max(temps), 2) if temps else None
        total_precip = round(sum(precips), 2) if precips else 0.0

        precip_last_7 = round(sum(precips[-7:]), 2) if len(precips) >= 7 else total_precip
        precip_last_14 = round(sum(precips[-14:]), 2) if len(precips) >= 14 else total_precip
        precip_last_30 = total_precip

        dry_spell = 0
        for p in reversed(precips):
            if p < 1.0:
                dry_spell += 1
            else:
                break

        gdd_cum = 0.0
        for d in dates_sorted:
            tmin = t2m_min_dict.get(d)
            tmax = t2m_max_dict.get(d)
            if tmin is not None and tmax is not None and tmin != -999 and tmax != -999:
                tavg = (tmin + tmax) / 2.0
                gdd_cum += max(0.0, tavg - 10.0)

        provenance = Provenance(
            provider=self.provider_id,
            provider_name=self.provider_name,
            capability=self.category,
            source_url="https://power.larc.nasa.gov/",
            observed_at=end_dt,
            data_quality=DataQuality.HISTORICAL_CLIMATE,
            freshness=FreshnessState.FRESH,
            attribution="Data from NASA POWER Agroclimate Program",
        )

        return ClimateData(
            period_label="Last 30 Days Agroclimate",
            mean_temp_c=mean_temp,
            min_temp_c=min_temp,
            max_temp_c=max_temp,
            total_precipitation_mm=total_precip,
            rainfall_7d_mm=precip_last_7,
            rainfall_14d_mm=precip_last_14,
            rainfall_30d_mm=precip_last_30,
            dry_spell_days=dry_spell,
            gdd_cumulative=round(gdd_cum, 1),
            et0_cumulative=None,
            anomalies={"rainfall_30d_vs_normal": round(total_precip - 80.0, 1)},
            provenance=provenance,
        )

    async def health_check(self) -> ProviderStatusInfo:
        start = time.perf_counter()
        try:
            dt_str = (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y%m%d")
            await transport.get_json(
                self.provider_id,
                self.base_url,
                params={"parameters": "T2M", "community": "AG", "longitude": 0, "latitude": 0, "start": dt_str, "end": dt_str, "format": "JSON"},
                timeout=5.0,
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
