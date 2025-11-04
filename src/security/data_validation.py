"""
data_validation.py

Validate incoming inventory/resource JSON objects.

This module provides a single helper function `data_validation` that checks
a Python dict against a JSON Schema tailored for the Inventory Tracking
System. The schema enforces required fields, types, the XOR rule that
exactly one of `location_id` or `employee_id` must be provided, and
additional simple constraints (e.g. `is_decommissioned` must be 0 or 1).

Behavior
- Returns True when validation succeeds.
- Returns False when validation fails.
- Prints small status messages on success/failure.

Schema summary
- type_id: integer (required)
- is_decommissioned: integer enum {0,1} (required)
- location_id: integer or null
- employee_id: integer or null
- notes: string or null
- Exactly one of (location_id, employee_id) must be present as an integer
  (enforced with JSON Schema `oneOf`).

Example
    >>> data = {
    ...     "type_id": 4,
    ...     "location_id": 1,
    ...     "employee_id": None,
    ...     "notes": "Test asset",
    ...     "is_decommissioned": 0
    ... }
    >>> data_validation(data)
    True
"""

import jsonschema
from jsonschema import validate
from src.logger import logger


def data_validation (data):
    # Define a schema
    schema = {
        "type": "object",
        "properties": {
            "type_id": {"type": "integer"},
            "location_id": {"type": ["integer", "null"]},
            "employee_id": {"type": ["integer", "null"]},
            "notes": {"type": ["string", "null"], "maxLength": 1000},
            "is_decommissioned": {"type": "integer", "enum": [0, 1]},
        },
        "required": ["type_id", "is_decommissioned"],
        # enforce exactly one of location_id or employee_id (XOR)
        "oneOf": [
            {
                "required": ["location_id"],
                "properties": {
                    "location_id": {"type": "integer"},
                    "employee_id": {"type": ["null"]}  # if present must be null
                }
            },
            {
                "required": ["employee_id"],
                "properties": {
                    "employee_id": {"type": "integer"},
                    "location_id": {"type": ["null"]}  # if present must be null
                }
            }
        ]
    }

    # Validate data
    try:
        validate(instance=data, schema=schema)
        logger.security("Data validation succeeded", level="warning")  
        return True
    except jsonschema.exceptions.ValidationError as e:
        logger.security(f"Data validation failed: {e.message}", level="warning")
        return False