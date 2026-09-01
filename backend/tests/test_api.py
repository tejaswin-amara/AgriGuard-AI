import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import create_db_and_tables

# Generate a small valid 1x1 black JPEG for testing
import io
from PIL import Image

img = Image.new("RGB", (1, 1), color="black")
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format="JPEG")
valid_jpeg_bytes = img_byte_arr.getvalue()

create_db_and_tables()
client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_disease_route():
    response = client.post(
        "/api/v1/disease/analyze",
        params={"crop": "tomato"},
        files={"image": ("leaf.jpg", valid_jpeg_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert data["is_demo"] is True


def test_soil_route():
    response = client.post(
        "/api/v1/soil/advise",
        json={
            "nitrogen": 40,
            "phosphorus": 30,
            "potassium": 20,
            "ph": 6.5,
            "moisture": 25,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_category" in data
    assert data["is_synthetic"] is True


def test_advisory_route():
    response = client.post(
        "/api/v1/advisory/generate",
        json={"source_reading_type": "soil", "source_reading_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "citations" in data
