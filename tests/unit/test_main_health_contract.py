import pytest
from fastapi.testclient import TestClient
from src.main import app

pytestmark = pytest.mark.unit

def test_health_returns_ok_and_logs(loguru_capture):
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    assert any("health" in rec.record["message"].lower() for rec in loguru_capture)
