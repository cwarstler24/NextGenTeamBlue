import pytest
import src.database.database_controller as dc
import src.database.authorize as db_auth

pytestmark = pytest.mark.unit

def test_add_resource_type_allows_manager_and_returns_200(monkeypatch):
    calls = {}
    def fake_exec(q, p=None):
        calls["query"] = q
        calls["params"] = p
        return {"status":"success", "rows_affected":1}
    monkeypatch.setattr(dc.database_connector, "execute_query", fake_exec)
    status = dc.add_resource_type({"asset_type_name": "Laptop"}, db_auth.Role.MANAGER)
    assert status == 200
    assert "INSERT INTO AssetTypes" in calls["query"]

def test_add_resource_type_denies_non_manager():
    assert dc.add_resource_type("Employee", {"asset_type_name":"Laptop"}) == 401

def test_add_resource_asset_creates_and_updates(monkeypatch):
    # 1) insert returns success
    # 2) select LAST_INSERT_ID returns new id
    # 3) fetch type name returns one row
    # 4) update returns success
    steps = []
    def fake_exec(q, p=None):
        steps.append(q.strip().split()[0].upper())
        if "LAST_INSERT_ID" in q:
            return [{"new_id": 7}]
        if "SELECT" in q and "FROM AssetTypes" in q:
            return [{"asset_type_name": "Laptop"}]
        return {"status":"success", "rows_affected":1}
    monkeypatch.setattr(dc.database_connector, "execute_query", fake_exec)
    status = dc.add_resource_asset({"type_id": 1, "location_id": 2,
                                                "employee_id": None, "notes": "",
                                                  "is_decommissioned": 0},
                                   db_auth.Role.MANAGER)
    assert status == 200
    # sanity: we called INSERT, SELECT (id), SELECT (type name),
    # UPDATE in some order
    assert "INSERT" in steps[0]
    assert any("SELECT" == s for s in steps)
    assert any("UPDATE" == s for s in steps)

def test_delete_resource_updates_flag(monkeypatch):
    called = {}
    monkeypatch.setattr(dc.database_connector, "execute_query",
                         lambda q, role, p=None: {"status":"success"})
    status = dc.delete_resource(10, db_auth.Role.MANAGER)
    assert status == 200

def test_update_resource_updates_fields(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                         lambda q, p=None: {"status":"success"})
    status = dc.update_resource({"asset_id":1,"type_id":2,
                                            "location_id":3,"employee_id":4,
                                            "notes":"","is_decommissioned":0},
                                db_auth.Role.MANAGER)
    assert status == 200

def test_get_resources_returns_tuple(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query", lambda q, p=None: [{"id":1}])
    code, items = dc.get_resources(db_auth.Role.MANAGER)
    assert code == 200 and items == [{"id":1}]

def test_get_resource_types_returns_tuple(monkeypatch):
    monkeypatch.setattr(dc.database_connector, "execute_query",
                        lambda q, p=None: [{"id":1,"asset_type_name":"Laptop"}])
    code, items = dc.get_resource_types(db_auth.Role.MANAGER)
    assert code == 200 and items and items[0]["asset_type_name"] == "Laptop"
