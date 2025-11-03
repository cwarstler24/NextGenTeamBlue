import asyncio
from types import SimpleNamespace
import pytest
from fastapi import HTTPException
import src.api.validate as v

pytestmark = pytest.mark.unit

class FakeRequest(SimpleNamespace):
    async def json(self):
        return self._json

def _req(method="GET", body=None):
    return FakeRequest(method=method, _json=body)

def test_missing_token_401():
    with pytest.raises(HTTPException) as ei:
        pytest.run(async_fn=v.validate_request(_req("GET"), token=""))
    assert ei.value.status_code == 401

def test_post_empty_body_400():
    with pytest.raises(HTTPException):
        pytest.run(async_fn=v.validate_request(_req("POST"), token="Bearer x"))

def test_post_schema_ok_with_location():
    body = {"type_id": 1, "location_id": 2, "employee_id": None, "notes": "", "is_decommissioned": 0}
    out = pytest.run(async_fn=v.validate_request(_req("POST", body), token="Bearer x"))
    assert out["status"] == "valid"

def test_post_schema_ok_with_employee():
    body = {"type_id": 1, "location_id": None, "employee_id": 5, "notes": None, "is_decommissioned": 1}
    out = pytest.run(async_fn=v.validate_request(_req("POST", body), token="Bearer x"))
    assert out["status"] == "valid"

def test_post_schema_fails_both_fields_present():
    body = {"type_id": 1, "location_id": 2, "employee_id": 5, "notes": "", "is_decommissioned": 0}
    with pytest.raises(HTTPException) as ei:
        pytest.run(async_fn=v.validate_request(_req("POST", body), token="Bearer x"))
    assert ei.value.status_code == 400
    assert "JSON validation error" in ei.value.detail

def test_put_schema_fails_neither_present():
    body = {"type_id": 1, "notes": "", "is_decommissioned": 0}
    with pytest.raises(HTTPException):
        pytest.run(async_fn=v.validate_request(_req("PUT", body), token="Bearer x"))

# small await helper
def _await(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
setattr(pytest, "run", _await)
