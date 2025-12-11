from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from src.logger import logger

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# SSO server configuration (read from environment, with sane default)
# Default points to host.docker.internal to reach services running on the host.
# On Linux, we rely on compose extra_hosts: host.docker.internal:host-gateway
SSO_SERVER_URL = os.getenv("SSO_SERVER_URL", "http://host.docker.internal:42068/login")

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str = None
    access_token: str = None
    bearerToken: str = None
    accessToken: str = None
    message: str = None

@router.post("/login")
async def proxy_login(credentials: LoginRequest):
    """
    Proxy endpoint that forwards login credentials to the SSO server.
    This acts as a bridge between the Vue frontend and SSO server.
    """
    logger.event(f"Login proxy called for user: {credentials.username}", level="info")
    
    try:
        # Forward the request to the SSO server
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                SSO_SERVER_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "username": credentials.username,
                    "password": credentials.password
                }
            )
        
        # Log the response status
        logger.security(
            f"SSO response status: {response.status_code} for user: {credentials.username}", 
            level="info"
        )
        
        # If SSO returns an error, forward it to the frontend
        if response.status_code not in (200, 201):
            error_detail = "Authentication failed"
            try:
                error_data = response.json()
                error_detail = error_data.get("message", error_data.get("detail", error_detail))
            except:
                pass
            
            logger.event(f"SSO authentication failed: {error_detail}", level="warning")
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        
        # Parse the SSO response
        sso_data = response.json()
        logger.event(f"Successful SSO authentication for user: {credentials.username}", level="info")
        
        # Return the SSO response to the frontend
        # The frontend expects fields like token, access_token, bearerToken, or accessToken
        return sso_data
        
    except httpx.RequestError as e:
        logger.event(f"SSO server connection error: {str(e)}", level="error")
        raise HTTPException(
            status_code=503, 
            detail="SSO server is unreachable. Please try again later."
        ) from e
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.event(f"Unexpected error during login proxy: {str(e)}", level="error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during authentication"
        ) from e
