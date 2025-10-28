import pytest
import sqlalchemy
import src.main as m

pytestmark = pytest.mark.integration

def test_health_ready_ok(client, monkeypatch, loguru_capture):
    # provide a fast, local engine
    sqlite_engine = sqlalchemy.create_engine("sqlite:///:memory:")
    monkeypatch.setattr(m, "get_engine", lambda: sqlite_engine)

    r = client.get("/health/ready")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["db"]["status"] == "up"
    # we should have an informational event log
    assert any("readiness probe result=ok" in rec.record["message"] for rec in loguru_capture)
