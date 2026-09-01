import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

from models.disease.inference import DiseaseInference

disease_inference = DiseaseInference()


def analyze_disease_image(image_bytes: bytes) -> dict:
    return disease_inference.predict(image_bytes)
