# src/validate.py
from fastapi import HTTPException, Request
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("API_SECRET_KEY", "defaultsecret")  # must match the key used when generating tokens

async def validate_request(request: Request, token: str):
    """
    Validates:
    1. Token readability (valid JWT format and signature)
    2. Body presence for POST/PUT requests
    """
    # --- Step 1: Token format ---
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format. Must start with 'Bearer '")

    token_value = token.split(" ")[1]

    # --- Step 2: Try decoding the token ---
    try:
        payload = jwt.decode(token_value, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # --- Step 3: For POST/PUT, check body ---
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
