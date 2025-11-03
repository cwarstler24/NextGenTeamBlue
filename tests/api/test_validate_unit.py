import pytest
from types import SimpleNamespace
from fastapi import HTTPException

from src.api import validate as v


class _Req:
    """
    Minimal async-friendly request stub:
      - .method
      - .json() -> awaits and returns provided body (or raises if None for POST/PUT)
    """
    def __init__(self, method: str, body: dict | None = None):
        self.method = method
        self._body = body

    async def json(self):
        if self._body is None:
            raise ValueError("No body")
        return self._body


def _req(method: str, body: dict | None = None):
    return _Req(method, body)


@pytest.mark.anyio
async def test_missing_token_401():
    with pytest.raises(HTTPException) as ei:
        await v.validate_request(_req("GET"), token="")
    assert ei.value.status_code == 401


@pytest.mark.anyio
async def test_post_empty_body_400():
    # POST with missing/invalid JSON body
    with pytest.raises(HTTPException) as ei:
        await v.validate_request(_req("POST"), token="Bearer x")
    assert ei.value.status_code == 400
    assert "invalid or missing json body" in ei.value.detail.lower() or "empty" in ei.value.detail.lower()


@pytest.mark.anyio
async def test_post_schema_ok_with_location():
    body = {"type_id": 1, "location_id": 2, "employee_id": None, "notes": "", "is_decommissioned": 0}
    out = await v.validate_request(_req("POST", body), token="Bearer x")
    assert out["status"] == "valid"


@pytest.mark.anyio
async def test_post_schema_ok_with_employee():
    body = {"type_id": 1, "location_id": None, "employee_id": 5, "notes": None, "is_decommissioned": 1}
    out = await v.validate_request(_req("POST", body), token="Bearer x")
    assert out["status"] == "valid"


@pytest.mark.anyio
async def test_post_schema_fails_both_fields_present():
    body = {"type_id": 1, "location_id": 2, "employee_id": 5, "notes": "", "is_decommissioned": 0}
    with pytest.raises(HTTPException) as ei:
        await v.validate_request(_req("POST", body), token="Bearer x")
    assert ei.value.status_code == 400
    assert "oneof" in ei.value.detail.lower() or "validation" in ei.value.detail.lower()


@pytest.mark.anyio
async def test_put_schema_fails_neither_present():
    body = {"type_id": 1, "notes": "", "is_decommissioned": 0}
    with pytest.raises(HTTPException):
        await v.validate_request(_req("PUT", body), token="Bearer x")
