# tests/integration/test_api_routes.py
import pytest
import sqlalchemy
import src.main as m

pytestmark = pytest.mark.integration

def test_health(client, loguru_capture):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    assert any("health check called" in rec.record["message"] for rec in loguru_capture)

def test_employees_count_uses_engine_mock(client, monkeypatch):
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("SELECT 1"))

    # Patch where it's USED now:
    monkeypatch.setattr(m, "get_db_connection", lambda: engine)

    r = client.get("/employees/count")
    assert r.status_code == 200
    assert r.json() == {"count": 1}
   