import pytest
import src.api.validate as v
import src.api.authenticate as a
import src.api.authorize as z
import src.database.database_controller as dc
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit

# --- Helpers to stub API dependencies ----------------------------------------

def _stub_validate_ok(*_args, **_kwargs):
    # Mimics src.api.validate.validate_request returning success
    return {"status": "valid", "method": "GET"}

def _stub_authenticate_employee(*_args, **_kwargs):
    # Mimics src.api.authenticate.authenticate_request
    return {"status": "valid", "method": "GET",
            "decoded_payload": {"sub": "u1", "title": "Employee",
                                "first_name": "E", "last_name": "User"}}

def _stub_authenticate_manager(*_args, **_kwargs):
    return {"status": "valid", "method": "POST",
            "decoded_payload": {"sub": "m1", "title": "Manager",
                                "first_name": "M", "last_name": "Boss"}}

def _stub_authorize_ok(*_args, **_kwargs):
    # Mimics src.api.authorize.authorize_request
    return {"authorized": True, "role": "Manager"}

# -----------------------------------------------------------------------------

def test_get_resources_happy_path(client, monkeypatch, loguru_capture):
    # Arrange: stub validation/auth/authz + DB
    monkeypatch.setattr(v, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(a, "authenticate_request", _stub_authenticate_employee, raising=True)
    monkeypatch.setattr(z, "authorize_request", _stub_authorize_ok, raising=True)
    monkeypatch.setattr(dc, "get_resources",
                        lambda: (200, [{"id": 1, "location": "HQ"}]),
                        raising=True)

    # Act
    r = client.get("/resources/", headers={"Authorization": "Bearer x"})
    # Assert
    assert r.status_code == 200
    assert r.json() == [{"id": 1, "location": "HQ"}]
    # (Optional) we don’t log in this route, but fixture logs start/end

def test_post_resource_manager_creates(client, monkeypatch, loguru_capture):    
    monkeypatch.setattr(v, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(a, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(z, "authorize_request", _stub_authorize_ok, raising=True)

    # db.add_resource_asset(title, body) → 200 means success
    calls = {}
    def fake_add(title, body):
        calls["title"] = title
        calls["body"] = body
        return 200

    monkeypatch.setattr(dc, "add_resource_asset", fake_add, raising=True)

    body = {"type_id": 1, "location_id": 2, "employee_id": None,
            "notes": "", "is_decommissioned": 0}
    r = client.post("/resources/", json=body, headers={"Authorization": "Bearer x"})

    assert r.status_code == 200
    assert r.text.strip('"') == "Resource Added"
    assert calls["title"] == "Manager"           # pulled from decoded payload
    assert calls["body"]["type_id"] == 1

def test_put_resource_manager_updates(client, monkeypatch):    
    monkeypatch.setattr(v, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(a, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(z, "authorize_request", _stub_authorize_ok, raising=True)

    # update_resource(title, body_with_asset_id) → 200 on success
    captured = {}
    def fake_update(title, body):
        captured["title"] = title
        captured["asset_id"] = body.get("asset_id")
        return 200

    monkeypatch.setattr(dc, "update_resource", fake_update, raising=True)

    body = {"type_id": 2, "location_id": 5, "employee_id": None,
            "notes": "changed", "is_decommissioned": 0}

    r = client.put("/resources/123", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == {"message": "Resource 123 updated successfully"}
    assert captured["title"] == "Manager"
    assert captured["asset_id"] == 123

def test_put_resource_db_failure_raises_400(client, monkeypatch):
    monkeypatch.setattr(v, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(a, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(z, "authorize_request", _stub_authorize_ok, raising=True)
    monkeypatch.setattr(dc, "update_resource", lambda *_: 400, raising=True)

    body = {"type_id": 1, "location_id": 2, "employee_id": None,
            "notes": "", "is_decommissioned": 0}

    r = client.put("/resources/42", json=body, headers={"Authorization": "Bearer x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Database update failed"

def test_delete_resource_manager_success(client, monkeypatch):
    monkeypatch.setattr(v, "validate_request", _stub_validate_ok, raising=True)
    monkeypatch.setattr(a, "authenticate_request", _stub_authenticate_manager, raising=True)
    monkeypatch.setattr(z, "authorize_request", _stub_authorize_ok, raising=True)

    monkeypatch.setattr(dc, "delete_resource", lambda *_: {"deleted": 1}, raising=True)

    r = client.delete("/resources/7", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert r.json() == {"deleted": 1}

# If you do NOT already have `client` in conftest.py, uncomment this:
# from src.app_factory import create_app
# @pytest.fixture()
# def client():
#     from fastapi.testclient import TestClient
#     app = create_app()
#     return TestClient(app)
