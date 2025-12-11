# src/authenticate.py
from fastapi import HTTPException, Request
import httpx
import os

# Prefer verifying against Rocket-Pop SSO by calling a protected endpoint with the token.
# If SSO_VERIFY_URL is set, we'll call that URL with Authorization header.
# Otherwise, fall back to the legacy AUTH_SERVER_URL.
SSO_VERIFY_URL = os.getenv("SSO_VERIFY_URL", "http://host.docker.internal:42068/user/info")
AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL", "http://172.16.0.51:8080/auth_service/api/auth/verify")

async def authenticate_request(request: Request, token: str):
    """Validate JWT tokens through the external authorization service and check request body."""   
    # --- Step 1: Basic token presence check ---
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # Remove "Bearer " prefix
    token_value = token.split(" ", 1)[1].strip()

    # --- Step 2: Authenticate token by calling SSO protected endpoint or legacy verifier ---
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if SSO_VERIFY_URL:
                # Call SSO with Authorization header; 200 means token accepted
                response = await client.get(
                    SSO_VERIFY_URL,
                    headers={
                        "Authorization": f"Bearer {token_value}",
                        "Accept": "application/json"
                    }
                )
            else:
                # Fallback: legacy auth service expects token in JSON
                response = await client.post(
                    AUTH_SERVER_URL,
                    headers={"Content-Type": "application/json"},
                    json={"token": token_value}
                )
    except httpx.RequestError as e:
        print("AUTH CONNECTION ERROR:", e)
        raise HTTPException(status_code=503, detail="Authorization service unreachable") from e

    # Log for debugging
    print("Auth response:", response.status_code, response.text)

    if response.status_code not in (200, 201):
        # SSO returns 200 on success; legacy may return 201
        raise HTTPException(status_code=401, detail="Unreadable or invalid token")

    # The verifier returns user info or the protected endpoint response; use it as decoded payload
    payload = response.json()

    # --- Step 3: Return success for next processing stage ---
    return {
        "status": "valid",
        "method": request.method,
        "decoded_payload": payload
    }
