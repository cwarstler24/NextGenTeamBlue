from __future__ import annotations
from fastapi import APIRouter, Request, Depends, HTTPException
from src.logger import logger

# Wrap your existing async functions so we can override them in tests
async def _validate_request_dep(request: Request, token: str):
    from src.validate import validate_request
    return await validate_request(request, token)

async def _authorize_request_dep(request: Request, decoded_payload: dict):
    from src.authenticate import authorize_request
    return await authorize_request(request, decoded_payload)

router = APIRouter(tags=["listener"])

@router.get("/")
async def root():
    return {"message": "Listener active on localhost"}

@router.api_route("/listener", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_request(
    validation_result = Depends(lambda req=Request: _validate_request_dep(req, req.headers.get("Authorization",""))),
    authorization_result = Depends(lambda req=Request, vr=Depends(lambda req=Request: _validate_request_dep(req, req.headers.get("Authorization",""))): _authorize_request_dep(req, vr["decoded_payload"])),
):
    token = Request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    decoded_payload = validation_result["decoded_payload"]

    logger.event(f"/listener {Request.method} validated", level="info")
    logger.security(f"/listener auth checked for {decoded_payload.get('sub','unknown')}", level="info")

    return {
        "method": Request.method,
        "path": str(Request.url),
        "user": f"{decoded_payload.get('first_name','')} {decoded_payload.get('last_name','')}".strip(),
        "role": authorization_result["role"],
        "validation_result": validation_result,
        "authorization_result": authorization_result
    }
