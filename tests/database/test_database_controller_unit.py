# tests/database/test_database_controller_more_unit.py
import types
import pytest
import src.database.database_controller as dc
from src.database import authorize as db_auth

pytestmark = pytest.mark.unit


def test_get_resource_by_id_success(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: [{"id": 7, "name": "A"}])
    code, item = dc.get_resource_by_id(7, db_auth.Role.MANAGER)
    assert code == 200 and item["id"] == 7


def test_get_resource_by_id_not_found(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: [])
    code, item = dc.get_resource_by_id(42, db_auth.Role.MANAGER)
    assert code == 400 and item == {}


def test_get_resource_by_employee_id_success(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: [{"id": 1}, {"id": 2}])
    code, items = dc.get_resource_by_employee_id(5, db_auth.Role.MANAGER)
    assert code == 200 and len(items) == 2


def test_get_resource_by_employee_id_failure(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: None)
    code, items = dc.get_resource_by_employee_id(5, db_auth.Role.MANAGER)
    assert code == 400 and items == []


def test_get_resource_by_location_id_success(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: [{"id": 3}])
    code, items = dc.get_resource_by_location_id(9, db_auth.Role.MANAGER)
    assert code == 200 and items[0]["id"] == 3


def test_get_resource_by_location_id_failure(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: None)
    code, items = dc.get_resource_by_location_id(9, db_auth.Role.MANAGER)
    assert code == 400 and items == []


def test_add_resource_asset_failure_on_insert(monkeypatch):
    # INSERT fails (returns None)
    monkeypatch.setattr(dc.database_connector, "execute_query", lambda q, p=None: None)
    status = dc.add_resource_asset({"type_id": 1, "location_id": 2,
                                    "employee_id": None, "notes": "",
                                    "is_decommissioned": 0}, 
                                   db_auth.Role.MANAGER)
    assert status == 400


def test_add_resource_asset_failure_on_last_insert_id(monkeypatch):
    # INSERT ok; LAST_INSERT_ID returns falsy
    steps = []
    def fake_exec(q, p=None):
        steps.append(q.strip().split()[0].upper())
        if "LAST_INSERT_ID" in q:
            return []   # simulate missing row
        return {"status": "success", "rows_affected": 1}
    monkeypatch.setattr(dc.database_connector, "execute_query", fake_exec)
    status = dc.add_resource_asset({"type_id": 1, "location_id": 2,
                                    "employee_id": None, "notes": "",
                                    "is_decommissioned": 0},
                                   db_auth.Role.MANAGER)
    assert status == 400


def test_add_resource_asset_failure_on_update_resource_id(monkeypatch):
    # INSERT ok; LAST_INSERT_ID ok; SELECT type ok; but final UPDATE fails
    def fake_exec(q, p=None):
        q_str = str(q)
        if "LAST_INSERT_ID" in q_str:
            return [{"new_id": 5}]
        if "FROM AssetTypes" in q_str:
            return [{"asset_type_name": "Monitor"}]
        # Be tolerant of newlines/spacing in the UPDATE statement
        if "UPDATE Asset" in q_str and "SET resource_id" in q_str:
            return None  # simulate failure in update_resource_id()
        return {"status": "success", "rows_affected": 1}

    import src.database.database_controller as dc
    monkeypatch.setattr(dc.database_connector, "execute_query", fake_exec)

    status = dc.add_resource_asset(
        {"type_id": 2, "location_id": 3, "employee_id": None, "notes": "", "is_decommissioned": 0},
        db_auth.Role.MANAGER
    )
    assert status == 400



def test_update_resource_id_success(monkeypatch):
    # Fix the year via monkeypatch (dc.datetime.datetime.now().year)
    class FakeDT(type(dc.datetime.datetime)):
        @classmethod
        def now(cls, tz=None):
            return dc.datetime.datetime(2031, 6, 1)

    # Patch datetime.datetime on the dc module
    monkeypatch.setattr(dc.datetime, "datetime",
                        type("FakeDateTime", (dc.datetime.datetime,), {"now": FakeDT.now}))

    def fake_exec(q, p=None):
        if "FROM AssetTypes" in q:
            return [{"asset_type_name": "Laptop"}]
        if "UPDATE Asset SET resource_id" in q:
            # ensure resource_id format is correct: <name>-<year>-<padded id>
            assert p["resource_id"] == "Laptop-2031-007"
            return {"status": "success", "rows_affected": 1}
        return {"status": "success", "rows_affected": 1}

    monkeypatch.setattr(dc.database_connector, "execute_query", fake_exec)
    ok = dc.update_resource_id(1, 7, db_auth.Role.MANAGER)
    assert ok is True


def test_update_resource_id_failure_when_type_missing(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q,
                        p=None: [] if "FROM AssetTypes" in q else {"status": "success"})
    ok = dc.update_resource_id(9, 100, db_auth.Role.MANAGER)
    assert ok is False
