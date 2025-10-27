# src/validate.py
from fastapi import HTTPException, Request
import jwt

async def validate_request(request: Request, token: str):
    """
    Validates that:
    1. The token exists and looks like a proper JWT.
    2. The request has a valid JSON body if it's a POST or PUT.
    """
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token_value = token.split(" ")[1]

    # --- Step 1: Check token structure (optional sanity check) ---
    parts = token_value.split(".")
    if len(parts) != 3:
        raise HTTPException(status_code=401, detail="Malformed token format")

    # --- Step 2: Try to read payload (without verifying signature) ---
    try:
        payload = jwt.decode(token_value, options={"verify_signature": False})
    except Exception:
        raise HTTPException(status_code=401, detail="Unreadable token")

    # --- Step 3: Check JSON body if applicable ---
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or missing JSON body")

        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")

    return {
        "status": "valid",
        "method": request.method,
        "decoded_payload": payload
    }
