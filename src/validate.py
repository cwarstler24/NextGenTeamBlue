# src/validate.py
from fastapi import HTTPException, Request
import jwt

async def validate_request(request: Request, token: str):
    """
    Validates:
    1. Token presence & structure.
    2. Required body fields and types for POST/PUT requests.
    """

    # --- Step 1: Token validation ---
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token_value = token.split(" ")[1]
    try:
        payload = jwt.decode(token_value, options={"verify_signature": False})
    except Exception:
        raise HTTPException(status_code=401, detail="Unreadable token")

    # --- Step 2: Validate JSON body for POST/PUT ---
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or missing JSON body")

        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")

        # Define expected schema
        required_fields = {
            "type_id": int,
            "location_id": int,
            "employee_id": int,
            "notes": str,
            "is_decommissoned": int
        }

        # --- Step 3: Check for missing fields ---
        missing = [field for field in required_fields if field not in body]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")

        # --- Step 4: Type validation ---
        for field, expected_type in required_fields.items():
            value = body[field]
            try:
                # Attempt to cast to correct type
                cast_value = expected_type(value)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' must be of type {expected_type.__name__} (got {type(value).__name__})"
                )

            # Optional: overwrite with casted version
            body[field] = cast_value

    return {
        "status": "valid",
        "method": request.method,
        "decoded_payload": payload
    }
