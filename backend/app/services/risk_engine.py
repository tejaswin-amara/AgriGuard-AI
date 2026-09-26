import logging
from app.schemas import RiskContextSchema, RiskSignal
from app.services.external.types import ClimateData, WeatherData

logger = logging.getLogger("agriguard.services.risk_engine")


class RiskEngine:
    """Combines environmental, meteorological, and climate context signals into qualitative agronomic indicators.

    Note: Does not manufacture false statistical probabilities. Uses qualitative pressure levels and explanations.
    """

    def evaluate(
        self,
        weather: WeatherData | None = None,
        climate: ClimateData | None = None,
        disease_confidence: float | None = None,
        disease_class: str | None = None,
        soil_ph: float | None = None,
        soil_moisture: float | None = None,
        elevation_m: float | None = None,
    ) -> RiskContextSchema:
        signals: list[RiskSignal] = []
        explanations: list[str] = []

        # 1. Fungal Pressure Signal
        fungal_level = "low"
        fungal_score = 0.2
        fungal_reasons = []

        temp = weather.temperature_c if weather else None
        humidity = weather.humidity_pct if weather else None
        precip = weather.rainfall_mm if weather else None
        soil_m = weather.soil_moisture_m3m3 if weather else soil_moisture

        if humidity is not None and humidity >= 75.0:
            fungal_score += 0.35
            fungal_reasons.append(f"High relative humidity ({humidity:.1f}%)")

        if temp is not None and 18.0 <= temp <= 32.0:
            fungal_score += 0.25
            fungal_reasons.append(f"Fungi-conducive ambient temperature ({temp:.1f}°C)")

        if precip is not None and precip >= 5.0:
            fungal_score += 0.25
            fungal_reasons.append(f"Recent precipitation ({precip:.1f}mm)")

        if soil_m is not None and soil_m >= 0.30:
            fungal_score += 0.15
            fungal_reasons.append("High upper-soil moisture level")

        fungal_score = min(1.0, round(fungal_score, 2))
        if fungal_score >= 0.75:
            fungal_level = "elevated"
        elif fungal_score >= 0.5:
            fungal_level = "moderate"

        signals.append(
            RiskSignal(
                name="fungal_pressure",
                level=fungal_level,
                score=fungal_score,
                explanation="; ".join(fungal_reasons) if fungal_reasons else "Normal humidity and moisture levels",
            )
        )
        if fungal_reasons:
            explanations.extend(fungal_reasons)

        # 2. Water Stress Signal
        water_level = "optimal"
        water_score = 0.1
        water_reasons = []

        rain_7d = climate.rainfall_7d_mm if climate else None
        dry_days = climate.dry_spell_days if climate else None
        et0 = weather.et0_mm if weather else None

        if dry_days is not None and dry_days >= 7:
            water_score += 0.4
            water_reasons.append(f"Extended dry spell ({dry_days} consecutive days without rain)")

        if rain_7d is not None and rain_7d < 5.0:
            water_score += 0.3
            water_reasons.append(f"Low 7-day cumulative rainfall ({rain_7d:.1f}mm)")

        if et0 is not None and et0 >= 5.0:
            water_score += 0.2
            water_reasons.append(f"High daily evapotranspiration demand (ET0 {et0:.1f}mm/day)")

        water_score = min(1.0, round(water_score, 2))
        if water_score >= 0.7:
            water_level = "severe"
        elif water_score >= 0.4:
            water_level = "moderate"

        signals.append(
            RiskSignal(
                name="water_stress",
                level=water_level,
                score=water_score,
                explanation="; ".join(water_reasons) if water_reasons else "Adequate precipitation and soil moisture",
            )
        )
        if water_reasons:
            explanations.extend(water_reasons)

        # 3. Heat Stress Signal
        heat_level = "none"
        heat_score = 0.0
        heat_reasons = []

        vpd = weather.vpd_kpa if weather else None
        if temp is not None and temp >= 35.0:
            heat_score += 0.6
            heat_reasons.append(f"High ambient temperature ({temp:.1f}°C)")

        if vpd is not None and vpd >= 2.0:
            heat_score += 0.3
            heat_reasons.append(f"High atmospheric Vapor Pressure Deficit ({vpd:.2f} kPa)")

        heat_score = min(1.0, round(heat_score, 2))
        if heat_score >= 0.6:
            heat_level = "high"
        elif heat_score >= 0.3:
            heat_level = "mild"

        signals.append(
            RiskSignal(
                name="heat_stress",
                level=heat_level,
                score=heat_score,
                explanation="; ".join(heat_reasons) if heat_reasons else "Ambient temperatures within normal crop tolerance",
            )
        )
        if heat_reasons:
            explanations.extend(heat_reasons)

        # Overall risk calculation
        overall_level = "low"
        if fungal_level == "elevated" or water_level == "severe" or heat_level == "high":
            overall_level = "elevated"
        elif fungal_level == "moderate" or water_level == "moderate" or heat_level == "mild":
            overall_level = "moderate"

        return RiskContextSchema(
            fungal_pressure=fungal_level,
            water_stress=water_level,
            heat_stress=heat_level,
            overall_level=overall_level,
            signals=signals,
            explanations=explanations,
        )


risk_engine = RiskEngine()
