import pytest
import sys
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

pytestmark = pytest.mark.unit

# Example: mimic your pattern for other routers
router = APIRouter()

class AssetCreate(BaseModel):
    type: str
    location: str

def get_service():
    # real app would inject a real service; tests can monkeypatch
    class Svc:
        def create(self, payload): return {"id": 1, **payload}
    return Svc()

@router.post("/assets", status_code=201)
def create_asset(body: AssetCreate, svc=Depends(get_service)):
    if body.type not in {"laptop", "monitor", "phone"}:
        raise HTTPException(status_code=400, detail="unsupported type")
    return svc.create(body.model_dump())

app = FastAPI()
app.include_router(router)

def test_assets_create_happy_path(monkeypatch):
    class Svc:
        def create(self, payload):
            return {"id": 99, **payload}
        
    # override the dependency FastAPI actually uses
    app.dependency_overrides[get_service] = lambda: Svc()
    try:
        client = TestClient(app)
        r = client.post("/assets", json={"type": "laptop", "location": "HQ"})
        assert r.status_code == 201
        assert r.json() == {"id": 99, "type": "laptop", "location": "HQ"}
    finally:
        app.dependency_overrides.clear()

def test_assets_create_rejects_bad_type():
    client = TestClient(app)
    r = client.post("/assets", json={"type":"toaster","location":"HQ"})
    assert r.status_code == 400
    assert r.json()["detail"] == "unsupported type"
