import asyncio
from types import SimpleNamespace
from fastapi import HTTPException
import pytest
import src.api.authorize as authz

pytestmark = pytest.mark.unit

def _req(method="GET"):
    return SimpleNamespace(method=method)

def test_manager_allows_all_methods():
    decoded = {"title": "Manager"}
    for m in ["GET", "POST", "PUT", "DELETE"]:
        out = pytest.run(async_fn=authz.authorize_request(_req(m), decoded))  # see helper below
        assert out["authorized"] is True
        assert out["role"] == "Manager"
        assert m in out["allowed_methods"]

def test_employee_get_ok_but_post_forbidden():
    decoded = {"title": "Employee"}
    out = pytest.run(async_fn=authz.authorize_request(_req("GET"), decoded))
    assert out["role"] == "Employee"
    with pytest.raises(HTTPException) as ei:
        pytest.run(async_fn=authz.authorize_request(_req("POST"), decoded))
    assert ei.value.status_code == 403

# --- tiny helper to await coroutines without importing anyio directly
def _await(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

setattr(pytest, "run", _await)
