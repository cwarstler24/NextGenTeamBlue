import asyncio
from types import SimpleNamespace
import pytest
from fastapi import HTTPException
import src.api.authenticate as auth

pytestmark = pytest.mark.unit

class DummyResp:
    def __init__(self, status_code=201, json_body=None, text="OK"):
        self.status_code = status_code
        self._json = json_body or {"sub":"u1","title":"Employee","first_name":"E","last_name":"U"}
        self.text = text
    def json(self): 
        return self._json

class FakeClient:
    def __init__(self, resp=None, raise_err=None):
        self._resp = resp or DummyResp()
        self._err = raise_err
    async def __aenter__(self): 
        return self
    async def __aexit__(self, *exc): 
        return False
    async def post(self, *_args, **_kwargs):
        if self._err:
            raise self._err
        return self._resp

def _await(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

setattr(pytest, "run", _await)

def test_authenticate_success(monkeypatch):
    monkeypatch.setattr(auth.httpx, "AsyncClient", lambda timeout: FakeClient(), raising=True)
    out = pytest.run(async_fn=auth.authenticate_request(SimpleNamespace(method="GET"), 
                                                        "Bearer abc"))
    assert out["status"] == "valid"
    assert out["decoded_payload"]["sub"] == "u1"

def test_authenticate_bad_header_401():
    with pytest.raises(HTTPException) as ei:
        pytest.run(async_fn=auth.authenticate_request(SimpleNamespace(method="GET"), "abc"))
    assert ei.value.status_code == 401

def test_authenticate_service_unreachable_503(monkeypatch):
    monkeypatch.setattr(auth.httpx, "AsyncClient",
                        lambda timeout: FakeClient(raise_err=auth.httpx.RequestError("boom")),
                        raising=True)
    with pytest.raises(HTTPException) as ei:
        pytest.run(async_fn=auth.authenticate_request(SimpleNamespace(method="GET"), "Bearer x"))
    assert ei.value.status_code == 503

def test_authenticate_invalid_token_401(monkeypatch):
    resp = DummyResp(status_code=401, text="nope")
    monkeypatch.setattr(auth.httpx, "AsyncClient", 
                        lambda timeout: FakeClient(resp=resp), raising=True)
    with pytest.raises(HTTPException) as ei:
        pytest.run(async_fn=auth.authenticate_request(SimpleNamespace(method="GET"), "Bearer x"))
    assert ei.value.status_code == 401
