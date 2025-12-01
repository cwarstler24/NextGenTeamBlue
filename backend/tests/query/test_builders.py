import pytest
from src.query.builders import build_asset_search_query

pytestmark = pytest.mark.unit

def test_build_asset_search_query_basic():
    sql, params = build_asset_search_query({"type":"laptop","location":"HQ","assigned":True})
    assert "SELECT * FROM assets WHERE" in sql
    assert "type = :type" in sql and "location = :location" in sql and "employee_id IS NOT NULL" in sql
    assert params == {"type":"laptop","location":"HQ"}

def test_build_asset_search_query_empty():
    sql, params = build_asset_search_query({})
    assert sql.strip().endswith("1=1")
    assert params == {}
