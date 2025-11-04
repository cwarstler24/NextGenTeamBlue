import pytest
from types import SimpleNamespace
from fastapi import HTTPException

from src.api import authorize as authz


def _req(method: str):
    # Minimal request object with only the attribute authz uses
    return SimpleNamespace(method=method)


@pytest.mark.anyio
async def test_manager_allows_all_methods():
    decoded = {"title": "Manager"}
    for m in ["GET", "POST", "PUT", "DELETE"]:
        out = await authz.authorize_request(_req(m), decoded)
        assert out["authorized"] is True
        assert "allowed" in out["action"].lower()


@pytest.mark.anyio
async def test_employee_get_ok_but_post_forbidden():
    decoded = {"title": "Employee"}

    # GET allowed
    out = await authz.authorize_request(_req("GET"), decoded)
    assert out["authorized"] is True
    assert out["role"] == "Employee"
    assert out["allowed_methods"] == ["GET"]

    # POST forbidden
    with pytest.raises(HTTPException) as ei:
        await authz.authorize_request(_req("POST"), decoded)
    assert ei.value.status_code == 403
    assert "only managers" in ei.value.detail.lower()
