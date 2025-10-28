from fastapi import HTTPException, Request
import httpx

# URL for the internal authorization service
AUTH_SERVER_URL = "http://172.16.0.51:8080/auth_service/api/auth/verify"

async def validate_request(request: Request, token: str):
    """Validate JWT tokens through the external authorization service and check request body."""
    
    # --- Step 1: Basic token presence check ---
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # Remove "Bearer " prefix
    token_value = token.split(" ", 1)[1].strip()

    # --- Step 2: Validate token via external auth service ---
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                AUTH_SERVER_URL,
                headers={"Content-Type": "application/json"},
                json={"token": token_value}
            )
    except httpx.RequestError as e:
        print("AUTH CONNECTION ERROR:", e)
        raise HTTPException(status_code=503, detail="Authorization service unreachable")

    # Log for debugging
    print("Auth response:", response.status_code, response.text)

    if response.status_code not in (200, 201): # authentication server sends a 201 instead of 200
        raise HTTPException(status_code=401, detail="Unreadable or invalid token")

    # The auth server returns verified user info
    payload = response.json()

    # --- Step 3: Validate JSON body for POST/PUT requests ---
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
            "location_id": int,
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

    # --- Step 4: Return success for next processing stage ---
    return {
        "status": "valid",
        "method": request.method,
        "decoded_payload": payload
    }
