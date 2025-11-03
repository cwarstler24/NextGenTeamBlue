import pytest
from fastapi.testclient import TestClient
import src.api.assets as assets

pytestmark = pytest.mark.unit

def test_create_asset_happy_uses_service(client):
    class FakeSvc(assets.AssetService):
        def create(self, payload):
            return {"id": 99, **payload}

    client.app.dependency_overrides[assets.get_service] = lambda: FakeSvc()
    try:
        r = client.post("/assets", json={"type": "laptop", "location": "HQ"})
        assert r.status_code == 201
        assert r.json() == {"id": 99, "type": "laptop", "location": "HQ"}
    finally:
        client.app.dependency_overrides.clear()

def test_create_asset_rejects_unsupported_type(client):
    r = client.post("/assets", json={"type": "toaster", "location": "HQ"})
    assert r.status_code == 400
    assert r.json()["detail"] == "unsupported type"
