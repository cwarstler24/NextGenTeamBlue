# tests/api/test_resources_routes_unit.py
from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from src.api.routes import resources as R

# --------- Async stubs used by our route ---------
async def _stub_validate_ok(request, token: str):
    # validate_request returns a simple confirmation in real code
    return {"status": "valid", "method": request.method}

async def _stub_authenticate_employee(request, token: str):
    # authenticate_request returns {"decoded_payload": <payload>}
    return {"decoded_payload": {"title": "Employee", "first_name": "Ada", "last_name": "Lovelace"}}

async def _stub_authenticate_manager(request, token: str):
    return {"decoded_payload": {"title": "Manager", "first_name": "Grace", "last_name": "Hopper"}}

async def _stub_authorize_ok(request, decoded_payload: dict):
    # authorize_request returns a dict but the route mainly needs it not to raise
    role = "Manager" if decoded_payload.get("title", "").lower() == "manager" else "Employee"
    return {"authorized": True, "role": role, "allowed_methods": [
        "GET", "POST", "PUT", "DELETE"], "action": f"{request.method} request allowed"}


# --- Helper to inject a fake db into the resources module ---
def _fake_db(**overrides):
    # defaults; you can override per test with keyword args
    funcs = {
        "get_resources": lambda: (200, [{"id": 1, "location": "HQ"}]),
        "add_resource_asset": lambda *_: 200,
        "update_resource": lambda *_: 200,
        "delete_resource": lambda *_: {"deleted": 1},
    }
    funcs.update(overrides)
    return SimpleNamespace(**funcs)


# -------------------- Tests --------------------

def test_get_resources_happy_path(client, monkeypatch, loguru_capture):
    # Patch inside the resources module (where symbols are used!)
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    # Patch db used by resources
    fake = _fake_db(get_resources=lambda: (200, [{"id": 1, "location": "HQ"}]))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == [{"id": 1, "location": "HQ"}]


def test_post_resource_manager_creates(client, monkeypatch, loguru_capture):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    calls = {}
    def fake_add(title, body):
        calls["title"] = title
        calls["body"] = body
        return 200

    fake = _fake_db(add_resource_asset=fake_add)
    monkeypatch.setattr(R, "db", fake, raising=True)

    body = {"type_id": 1, "location_id": 2, "employee_id": None,
            "notes": "", "is_decommissioned": 0}
    r = client.post("/resources/", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == "Resource Added"
    assert calls["title"] == "Manager"  # taken from decoded_payload["title"]
    assert calls["body"]["type_id"] == 1


def test_put_resource_manager_updates(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    captured = {}
    def fake_update(title, body):
        captured["title"] = title
        captured["asset_id"] = body.get("asset_id")
        return 200

    fake = _fake_db(update_resource=fake_update)
    monkeypatch.setattr(R, "db", fake, raising=True)

    body = {"type_id": 2, "location_id": 5, "employee_id": None,
            "notes": "changed", "is_decommissioned": 0}

    r = client.put("/resources/123", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 200, r.text
    assert r.json()["message"] == "Resource 123 updated successfully"
    assert captured["title"] == "Manager"
    assert captured["asset_id"] == 123


def test_put_resource_db_failure_raises_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(update_resource=lambda *_: 400)
    monkeypatch.setattr(R, "db", fake, raising=True)

    body = {"type_id": 1, "location_id": 2, "employee_id": None,
            "notes": "", "is_decommissioned": 0}

    r = client.put("/resources/42", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database update failed"


def test_delete_resource_manager_success(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(delete_resource=lambda *_: {"deleted": 1})
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.delete("/resources/7", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == {"deleted": 1}
