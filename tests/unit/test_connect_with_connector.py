# tests/unit/test_connect_with_connector.py
import pytest
from types import SimpleNamespace

pytestmark = pytest.mark.unit

def test_connect_with_connector_uses_connector_creator(monkeypatch):
    calls = {}

    # fake connector.connect returning a dummy conn object
    class FakeConnector:
        def connect(self, instance, driver, user, password, db, ip_type):
            calls["connect_args"] = (instance, driver, user, password, db, str(ip_type))
            return object()

    # spy on sqlalchemy.create_engine to capture "creator"
    def fake_create_engine(url, creator):
        calls["url"] = url
        calls["creator_returns"] = creator()  # call it once to ensure callable
        return SimpleNamespace()  # fake engine

    import src.main as m
    monkeypatch.setattr(m, "Connector", lambda: FakeConnector())
    monkeypatch.setattr(m.sqlalchemy, "create_engine", fake_create_engine)

    engine = m.connect_with_connector()
    assert isinstance(engine, SimpleNamespace)
    assert calls["url"] == "mysql+pymysql://"
    # ensure connector.connect was wired with parameters
    instance, driver, user, password, db, ip_type = calls["connect_args"]
    assert driver == "pymysql"
    assert user and password and db
