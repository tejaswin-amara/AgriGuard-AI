import os

os.environ["DATABASE_URL"] = "sqlite:///./test_agriguard.db"

import io

from fastapi.testclient import TestClient
from PIL import Image

from app.db.session import create_db_and_tables
from app.main import app

# Generate a small valid 1x1 black JPEG for testing
img = Image.new("RGB", (1, 1), color="black")
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format="JPEG")
valid_jpeg_bytes = img_byte_arr.getvalue()

create_db_and_tables()
client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] in ("healthy", "degraded", "ok")


def test_disease_route():
    response = client.post(
        "/api/v1/disease/analyze",
        data={"crop": "tomato"},
        files={"file": ("leaf.jpg", valid_jpeg_bytes, "image/jpeg")},
    )
    assert response.status_code == 201
    data = response.json()
    assert "predicted_class" in data
    assert data["is_demo"] is True
    assert "model_provenance" in data


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
    assert response.status_code == 201
    data = response.json()
    assert "predicted_category" in data
    assert data["is_synthetic"] is True
    assert "model_provenance" in data


def test_advisory_route():
    response = client.post(
        "/api/v1/advisory/generate",
        json={"source_reading_type": "soil", "source_reading_id": 1},
    )
    assert response.status_code == 201
    data = response.json()
    assert "recommendation" in data
    assert "citations" in data


def test_farm_and_context_routes():
    # 1. Create farm
    create_resp = client.post(
        "/api/v1/farms",
        json={
            "name": "Nizamabad Cotton Farm",
            "location_query": "Nizamabad, Telangana",
            "primary_crop": "Cotton",
        },
    )
    assert create_resp.status_code == 201
    farm = create_resp.json()
    assert farm["name"] == "Nizamabad Cotton Farm"
    farm_id = farm["id"]

    # 2. Get farm
    get_resp = client.get(f"/api/v1/farms/{farm_id}")
    assert get_resp.status_code == 200

    # 3. Get farm context
    ctx_resp = client.get(f"/api/v1/farms/{farm_id}/context")
    assert ctx_resp.status_code == 200
    ctx_data = ctx_resp.json()
    assert "weather" in ctx_data
    assert "climate" in ctx_data
    assert "risk_context" in ctx_data


def test_providers_route():
    resp = client.get("/api/v1/providers")
    assert resp.status_code == 200
    providers = resp.json()
    assert len(providers) >= 3


def test_news_route():
    resp = client.get("/api/v1/news")
    assert resp.status_code == 200
    news = resp.json()
    assert "articles" in news


def test_cors_headers_restricted():
    # Allowed origin returns CORS headers
    resp_allowed = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert (
        resp_allowed.headers.get("access-control-allow-origin")
        == "http://localhost:5173"
    )

    # Disallowed origin does NOT return CORS header
    resp_disallowed = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://malicious-domain.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert (
        resp_disallowed.headers.get("access-control-allow-origin")
        != "http://malicious-domain.com"
    )
