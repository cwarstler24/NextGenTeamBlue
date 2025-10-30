# src/query/builders.py
from typing import Tuple, Dict, Any

def build_asset_search_query(filters: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Return a SQL fragment + params (DB-agnostic) for simple asset search."""
    clauses, params = [], {}
    if t := filters.get("type"):
        clauses.append("type = :type")
        params["type"] = t
    if loc := filters.get("location"):
        clauses.append("location = :location")
        params["location"] = loc
    if "assigned" in filters:
        clauses.append("employee_id IS NOT NULL" if filters["assigned"] else "employee_id IS NULL")
    where = " AND ".join(clauses) or "1=1"
    return f"SELECT * FROM assets WHERE {where}", params
