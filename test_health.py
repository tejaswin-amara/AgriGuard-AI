"""Smoke tests. Deliberately minimal — these prove the scaffold boots and
the stub contracts behave as documented, not that the product works yet.
"""

import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_disease_route_honestly_reports_not_implemented():
    response = client.post(
        "/api/v1/disease/analyze",
        params={"crop": "tomato"},
        files={"image": ("leaf.jpg", b"fake-bytes", "image/jpeg")},
    )
    assert response.status_code == 501


def test_soil_route_honestly_reports_not_implemented():
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
    assert response.status_code == 501


def test_advisory_route_honestly_reports_not_implemented():
    response = client.post(
        "/api/v1/advisory/generate",
        json={"source_reading_type": "soil", "source_reading_id": 1},
    )
    assert response.status_code == 501
