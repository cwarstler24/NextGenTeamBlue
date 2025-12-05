import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.assets import get_service

pytestmark = pytest.mark.unit

def test_create_asset_happy_path():
    class Svc:
        def create(self, payload): return {"id": 99, **payload}

    app.dependency_overrides[get_service] = lambda: Svc()
    try:
        client = TestClient(app)
        r = client.post("/assets", json={"type":"laptop","location":"HQ"})
        assert r.status_code == 201
        assert r.json() == {"id": 99, "type":"laptop","location":"HQ"}
    finally:
        app.dependency_overrides.clear()

def test_create_asset_rejects_bad_type():
    client = TestClient(app)
    r = client.post("/assets", json={"type":"toaster","location":"HQ"})
    assert r.status_code == 400
    assert r.json()["detail"] == "unsupported type"
