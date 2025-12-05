# tests/api/test_resources_routes_unit.py
from types import SimpleNamespace
import pytest
from src.api.routes import resources as R
from src.database import authorize as db_auth

pytestmark = pytest.mark.unit

# --------- Async stubs used by our route ---------
async def _stub_validate_ok(request, token: str):
    return {"status": "valid", "method": request.method}

async def _stub_authenticate_employee(request, token: str):
    return {"decoded_payload": {"title": "Employee", "first_name": "Ada", "last_name": "Lovelace"}}

async def _stub_authenticate_manager(request, token: str):
    return {"decoded_payload": {"title": "Manager", "first_name": "Grace", "last_name": "Hopper"}}

async def _stub_authorize_ok(request, decoded_payload: dict):
    role = "Manager" if decoded_payload.get("title", "").lower() == "manager" else "Employee"
    return {"authorized": True, "role": role, "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
            "action": f"{request.method} request allowed"}

# --- Helper to inject a fake db into the resources module ---
def _fake_db(**overrides):
    funcs = {
        "get_resources": lambda: (200, [{"id": 1, "location": "HQ"}]),
        "get_resource_types": lambda: (200, [{"id": 9, "asset_type_name": "Laptop"}]),
        "get_resource_by_id": lambda rid: (200, {"id": rid, "location": "HQ"}),
        "get_resource_by_employee_id": lambda eid: (200, [{"id": 2, "employee_id": eid}]),
        "get_resource_by_location_id": lambda lid: (200, [{"id": 3, "location_id": lid}]),
        "add_resource_asset": lambda *_: 200,
        "update_resource": lambda *_: 200,
        "delete_resource": lambda *_: 200,
    }
    funcs.update(overrides)
    return SimpleNamespace(**funcs)


# -------------------- Happy paths --------------------

def test_get_resources_happy_path(client, monkeypatch, loguru_capture):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resources=lambda role: (200, [{"id": 1, "location": "HQ"}]))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == [{"id": 1, "location": "HQ"}]


def test_get_resource_types_happy_path(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_types=lambda role: (200, [{"id": 4, "asset_type_name": "Monitor"}]))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/types/", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == [{"id": 4, "asset_type_name": "Monitor"}]


def test_get_resource_by_id_happy_path(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_by_id=lambda rid, role: (200, {"id": rid, "location": "HQ"}))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/123", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == {"id": 123, "location": "HQ"}


def test_get_resources_by_employee_happy_path(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_by_employee_id=lambda eid, role: (200, [{"id": 7, "employee_id": eid}]))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/employee/55", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == [{"id": 7, "employee_id": 55}]


def test_get_resources_by_location_happy_path(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_by_location_id=lambda lid, role: (200, [{"id": 8, "location_id": lid}]))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/location/77", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == [{"id": 8, "location_id": 77}]


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

    # ensure sanitize_data is invoked; patch it to prove call
    monkeypatch.setattr(R, "sanitize_data", lambda s: f"SANITIZED({s})", raising=True)

    body = {"type_id": 1, "location_id": 2, "employee_id": None,
            "notes": "<b>note</b>", "is_decommissioned": 0}
    r = client.post("/resources/", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == "Resource Added Successfully"
    assert calls['body'] == db_auth.Role.MANAGER  # taken from decoded_payload["title"]:Warning
    # notes got sanitized
    assert calls["title"]["notes"] == "SANITIZED(<b>note</b>)"


def test_put_resource_manager_updates(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    captured = {}
    def fake_update(body, title):
        captured["title"] = title
        captured["asset_id"] = body.get("asset_id")
        captured["notes"] = body.get("notes")
        return 200

    fake = _fake_db(update_resource=fake_update)
    monkeypatch.setattr(R, "db", fake, raising=True)

    monkeypatch.setattr(R, "sanitize_data", lambda s: f"OK({s})", raising=True)

    body = {"type_id": 2, "location_id": 5, "employee_id": None,
            "notes": "changed", "is_decommissioned": 0}
    r = client.put("/resources/123", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 200, r.text
    assert r.json()["message"] == "Resource 123 updated successfully"
    assert captured["title"] == db_auth.Role.MANAGER
    assert captured["asset_id"] == 123
    assert captured["notes"] == "OK(changed)"


def test_delete_resource_manager_success(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(delete_resource=lambda *_: 200)
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.delete("/resources/7", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == "Resource deleted successfully"


# -------------------- Error paths --------------------

def test_missing_token_401_all_paths(client):
    # a few representative endpoints
    for method, url in [
        ("GET", "/resources/"),
        ("GET", "/resources/types/"),
        ("GET", "/resources/123"),
        ("GET", "/resources/employee/5"),
        ("GET", "/resources/location/9"),
        ("POST", "/resources/"),
        ("PUT", "/resources/1"),
        ("DELETE", "/resources/1"),
    ]:
        if method == "GET":
            resp = client.get(url)  # no Authorization header
        elif method == "POST":
            resp = client.post(url, json={})
        elif method == "PUT":
            resp = client.put(url, json={})
        else:
            resp = client.delete(url)
        assert resp.status_code == 401, f"{method} {url} should be 401"
        assert resp.json()["detail"] == "Missing Authorization header"


def test_get_resources_db_error_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resources=lambda role: (400, []))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/", headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database error"


def test_get_resource_types_db_error_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_types=lambda role: (400, []))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/types/", headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database error"


def test_get_resource_by_id_404_when_missing(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_by_id=lambda rid, role: (400, {}))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/777", headers={"Authorization": "Bearer x"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Resource not found"


def test_get_resources_by_employee_db_error_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_by_employee_id=lambda eid, role: (400, []))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/employee/22", headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database error"


def test_get_resources_by_location_db_error_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(get_resource_by_location_id=lambda lid, role: (400, []))
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.get("/resources/location/33", headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database error"


def test_post_resource_db_error_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(add_resource_asset=lambda *_: 400)
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.post("/resources/", json={"type_id": 1, "location_id": 2, "employee_id": None,
                                         "notes": "", "is_decommissioned": 0},
                    headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database error"


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


def test_delete_resource_db_failure_400(client, monkeypatch):
    monkeypatch.setattr(R, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(R, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(R, "authorize_request", _stub_authorize_ok, raising=True)

    fake = _fake_db(delete_resource=lambda *_: 400)
    monkeypatch.setattr(R, "db", fake, raising=True)

    r = client.delete("/resources/7", headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database delete failed"
