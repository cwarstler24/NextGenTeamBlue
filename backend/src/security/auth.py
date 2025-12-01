# src/security/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=False)

def validate_token(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    if not creds or creds.scheme.lower() != "bearer" or creds.credentials != "DEV-TOKEN":
        raise HTTPException(status_code=401, detail="unauthorized")
    return {"sub": "dev-user"}
