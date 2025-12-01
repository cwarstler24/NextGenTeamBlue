import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from src.security.auth import validate_token

pytestmark = pytest.mark.unit

app = FastAPI()
@app.get("/secure")
def secure(user = Depends(validate_token)):
    return {"ok": True, "user": user["sub"]}

def test_secure_unauthorized():
    client = TestClient(app)
    assert client.get("/secure").status_code == 401

def test_secure_authorized():
    client = TestClient(app)
    r = client.get("/secure", headers={"Authorization": "Bearer DEV-TOKEN"})
    assert r.status_code == 200 and r.json()["ok"] is True
