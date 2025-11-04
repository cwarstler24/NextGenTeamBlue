from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.api.validate import validate_request
from src.api.authenticate import authenticate_request
from src.api.authorize import authorize_request
from src.security.sanitize import sanitize_data
import src.database.database_controller as db
from src.utils import convert_bytes_to_strings
from src.logger import logger

router = APIRouter(prefix="/resources", tags=["Resources"])

# --- GET /resources ---
@router.get("/")
async def get_resources(request: Request):
    logger.event("GET /resources", level="info")
    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Missing Authorization header", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    logger.event("Validating request", level="info")
    await validate_request(request, token)
    logger.event("Authenticating request", level="info")
    auth_result = await authenticate_request(request, token)

    decoded = auth_result["decoded_payload"]
    logger.event("Authorizing request", level="info")
    await authorize_request(request, decoded)

    result = db.get_resources()

    if result[0] == 200:
        logger.event("Returning resources", level="info")
        return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)
    else:
        logger.event("Returning error 400", level="error")
        raise HTTPException(status_code=400, detail="Database error")

# --- GET /resources/types/ ---
@router.get("/types/")
async def get_resource_types(request: Request):
    logger.event("GET /resources/types", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_types()

    if result[0] == 200:
        logger.event("Returning resource types", level="info")
        return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)

    logger.event("Returning error 400", level="error")
    raise HTTPException(status_code=400, detail="Database error")

# --- GET /resources/{resource_id} ---
@router.get("/{resource_id}")
async def get_resource_by_id(request: Request, resource_id: int):
    logger.event(f"GET /resources/{resource_id}", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_by_id(resource_id)

    if result[0] == 200:
        logger.event("Returning resource", level="info")
        return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)

    logger.event("Returning error 404", level="error")
    raise HTTPException(status_code=404, detail="Resource not found")


# --- GET /resources/employee/{employee_id} ---
@router.get("/employee/{employee_id}")
async def get_resources_by_employee(request: Request, employee_id: int):
    logger.event(f"GET /resources/employee/{employee_id}", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_by_employee_id(employee_id)
    if result[0] == 200:
        logger.event("Returning resources", level="info")
        return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)
    else:
        logger.event("Returning error 400", level="error")
        raise HTTPException(status_code=400, detail="Database error")


# --- GET /resources/location/{location_id} ---
@router.get("/location/{location_id}")
async def get_resources_by_location(request: Request, location_id: int):
    logger.event(f"GET /resources/location/{location_id}", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_by_location_id(location_id)
    if result[0] == 200:
        logger.event("Returning resources", level="info")
        return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)
    else:
        logger.event("Returning error 400", level="error")
        raise HTTPException(status_code=400, detail="Database error")


# --- POST /resources ---
@router.post("/")
async def post_resource(request: Request):
    logger.event("POST /resources", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    body = await request.json()

    # Sanitize notes field
    if "notes" in body and body["notes"] is not None:
        body["notes"] = sanitize_data(body["notes"])

    result = db.add_resource_asset(decoded.get("title", ""), body)
    if result == 200:
        message = "Resource added successfully"
        logger.event(f"Returning success 200: {message}", level="info")
        return JSONResponse(content={"message": message}, status_code=200)
    elif result == 400:
        message = "Database error"
        logger.event(f"Returning error 400: {message}", level="error")
        raise HTTPException(status_code=400, detail=message)


# --- PUT /resources/{id} ---
@router.put("/{id}")
async def update_resource(request: Request, id: int):
    logger.event(f"PUT /resources/{id}", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    body = await request.json()
    body["asset_id"] = id

    # Sanitize notes
    if "notes" in body and body["notes"] is not None:
        body["notes"] = sanitize_data(body["notes"])

    result = db.update_resource(decoded.get("title", ""), body)
    if result == 200:
        message = f"Resource {id} updated successfully"
        logger.event(f"Returning success 200: {message}", level="info")
        return JSONResponse(content={"message": message}, status_code=200)
    else:
        message = "Database update failed"
        logger.event(f"Returning error 400 {message}", level="error")
        raise HTTPException(status_code=400, detail=message)

# --- DELETE /resources/{id} ---
@router.delete("/{id}")
async def delete_resource(request: Request, id: int):
    logger.event(f"DELETE /resources/{id}", level="info")

    token = request.headers.get("Authorization")
    logger.security(f"token: {token}", level="trace")
    if not token:
        logger.event("Returning error 401: no token", level="warning")
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    # Expect the DB layer to return something like {"deleted": 1}
    result = db.delete_resource(decoded.get("title", ""), id)
    if result == 200:
        message = f"Resource {id} deleted successfully"
        logger.event(f"Returning success 200: {message}", level="info")
        return JSONResponse(content={"message": message}, status_code=200)
    else:
        message = "Database delete failed"
        logger.event(f"Returning error 400 {message}", level="error")
        raise HTTPException(status_code=400, detail=message)
