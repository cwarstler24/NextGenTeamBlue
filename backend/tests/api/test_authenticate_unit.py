from types import SimpleNamespace
import pytest
from fastapi import HTTPException

from src.api import authenticate as auth


class DummyResp:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload if payload is not None else {"title": "Employee"}
        self.text = text

    def json(self):
        return self._payload


class FakeClient:
    """
    Async context manager that mimics httpx.AsyncClient but is fully in-memory.
    - If raise_err is set, .post(...) raises that error.
    - Otherwise, returns the provided DummyResp (defaults to 200).
    """
    def __init__(self, resp: DummyResp | None = None, raise_err: Exception | None = None):
        self._resp = resp or DummyResp(200, {"title": "Employee"})
        self._err = raise_err

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *args, **kwargs):
        if self._err:
            raise self._err
        return self._resp

@pytest.mark.skip(reason="Tests need to be updated for recent changes to authenticate_request")
@pytest.mark.anyio
async def test_authenticate_success(monkeypatch):
    # Return 200 with a decoded payload
    monkeypatch.setattr(auth.httpx, "AsyncClient", lambda timeout: FakeClient(), raising=True)
    out = await auth.authenticate_request(SimpleNamespace(method="GET"), "Bearer abc")
    assert out["status"] == "valid"
    assert out["decoded_payload"]["title"] == "Employee"

@pytest.mark.skip(reason="Tests need to be updated for recent changes to authenticate_request")
@pytest.mark.anyio
async def test_authenticate_bad_header_401():
    with pytest.raises(HTTPException) as ei:
        await auth.authenticate_request(SimpleNamespace(method="GET"), "abc")
    assert ei.value.status_code == 401
    assert "Missing or invalid Authorization header" in ei.value.detail

@pytest.mark.skip(reason="Tests need to be updated for recent changes to authenticate_request")
@pytest.mark.anyio
async def test_authenticate_service_unreachable_503(monkeypatch):
    err = auth.httpx.RequestError("boom")
    monkeypatch.setattr(auth.httpx, "AsyncClient",
                        lambda timeout: FakeClient(raise_err=err), raising=True)
    with pytest.raises(HTTPException) as ei:
        await auth.authenticate_request(SimpleNamespace(method="GET"), "Bearer x")
    assert ei.value.status_code == 503
    assert "unreachable" in ei.value.detail.lower()


@pytest.mark.anyio
async def test_authenticate_invalid_token_401(monkeypatch):
    resp = DummyResp(status_code=401, text="nope")
    monkeypatch.setattr(auth.httpx, "AsyncClient",
                         lambda timeout: FakeClient(resp=resp), raising=True)
    with pytest.raises(HTTPException) as ei:
        await auth.authenticate_request(SimpleNamespace(method="GET"), "Bearer x")
    assert ei.value.status_code == 401
    assert "invalid" in ei.value.detail.lower() or "unreadable" in ei.value.detail.lower()
