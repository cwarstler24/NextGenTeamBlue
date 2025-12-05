import pytest
import sqlalchemy
import src.api.health as health

pytestmark = pytest.mark.unit

def test_health_logs_and_ok(client, loguru_capture):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    assert any("health check called" in rec.record["message"] for rec in loguru_capture)

def test_health_ready_ok(client, monkeypatch, loguru_capture):
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("SELECT 1"))
    monkeypatch.setattr(health, "get_db_connection", lambda: engine, raising=True)

    r = client.get("/health/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["db"]["status"] == "up"

def test_health_ready_down(client, monkeypatch, loguru_capture):
    class Boom:
        def connect(self):
            raise RuntimeError("db down")
    monkeypatch.setattr(health, "get_db_connection", lambda: Boom(), raising=True)

    r = client.get("/health/ready")
    assert r.status_code == 503
    data = r.json()
    assert data["status"] == "error"
    assert data["db"]["status"] == "down"
    assert any("readiness db check FAILED" in rec.record["message"] for rec in loguru_capture)
