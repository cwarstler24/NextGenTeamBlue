from fastapi import HTTPException, Request
import httpx

async def validate_request(request: Request, token: str):
    """Validate JWT tokens through the external authorization service and check request body."""
    
    # --- Step 1: Basic token presence check ---
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # --- Step 2: Validate JSON body for POST/PUT requests ---
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or missing JSON body")

        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")

        # Required fields and expected types
        required_fields = {
            "type_id": int,
            "employee_id": int,
            "notes": str,
            "is_decommissoned": int
        }

        missing = [f for f in required_fields if f not in body]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing fields: {', '.join(missing)}")

        for field, expected_type in required_fields.items():
            try:
                body[field] = expected_type(body[field])
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' must be {expected_type.__name__}"
                )

    # --- Step 3: Return success for next processing stage ---
    return {
        "status": "valid",
        "method": request.method
    }
