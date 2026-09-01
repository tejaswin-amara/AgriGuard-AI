import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

from models.soil.inference import SoilInference
from app.schemas import SoilAdviseRequest

soil_inference = SoilInference()


def advise_soil_readings(readings: SoilAdviseRequest) -> dict:
    return soil_inference.predict(
        n=readings.nitrogen,
        p=readings.phosphorus,
        k=readings.potassium,
        ph=readings.ph,
        moisture=readings.moisture,
    )
