from fastapi import HTTPException, Request
import httpx
import jsonschema
from jsonschema import validate as json_validate

async def validate_request(request: Request, token: str):
    """
    Validates an incoming API request.
    - Ensures token format is valid.
    - Validates body fields for POST and PUT requests.
    - Enforces XOR rule: exactly one of location_id or employee_id must be provided.
    Raises HTTPException on validation failure.
    """

    # --- Step 1: Validate token header ---
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # --- Step 2: For POST/PUT, validate JSON body against schema ---
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or missing JSON body")

        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")

        # Define JSON schema (based on teammate’s rules)
        schema = {
            "type": "object",
            "properties": {
                "type_id": {"type": "integer"},
                "location_id": {"type": ["integer", "null"]},
                "employee_id": {"type": ["integer", "null"]},
                "notes": {"type": ["string", "null"]},
                "is_decommissioned": {"type": "integer", "enum": [0, 1]},
            },
            "required": ["type_id", "is_decommissioned"],
            "oneOf": [
                {
                    "required": ["location_id"],
                    "properties": {
                        "location_id": {"type": "integer"},
                        "employee_id": {"type": ["null"]}
                    }
                },
                {
                    "required": ["employee_id"],
                    "properties": {
                        "employee_id": {"type": "integer"},
                        "location_id": {"type": ["null"]}
                    }
                }
            ]
        }

        # --- Step 3: Validate JSON data against schema ---
        try:
            json_validate(instance=body, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            # Format message to be concise
            raise HTTPException(
                status_code=400,
                detail=f"JSON validation error: {e.message}"
            )

    # --- Step 4: Return confirmation if everything passes ---
    return {
        "status": "valid",
        "method": request.method
    }
