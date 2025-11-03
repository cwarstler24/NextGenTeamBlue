from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.api.validate import validate_request
from src.api.authenticate import authenticate_request
from src.api.authorize import authorize_request
import src.database.database_controller as db
from src.utils import convert_bytes_to_strings

router = APIRouter(prefix="/resources", tags=["Resources"])

# --- GET /resources ---
@router.get("/")
async def get_resources(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resources()
    return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)

# --- GET /resources/types/ ---
@router.get("/types/")
async def get_resource_types(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_types()
    return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)

# --- GET /resources/{resource_id} ---
@router.get("/{resource_id}")
async def get_resource_by_id(request: Request, resource_id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_by_id(resource_id)
    if not result or not result[1]:
        raise HTTPException(status_code=404, detail="Resource not found")

    return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)


# --- GET /resources/employee/{employee_id} ---
@router.get("/employee/{employee_id}")
async def get_resources_by_employee(request: Request, employee_id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_by_employee_id(employee_id)
    if not result or not result[1]:
        raise HTTPException(status_code=404, detail="No resources found for this employee")

    return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)


# --- GET /resources/location/{location_id} ---
@router.get("/location/{location_id}")
async def get_resources_by_location(request: Request, location_id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    result = db.get_resource_by_location_id(location_id)
    if not result or not result[1]:
        raise HTTPException(status_code=404, detail="No resources found for this location")

    return JSONResponse(content=convert_bytes_to_strings(result[1]), status_code=status.HTTP_200_OK)


# --- POST /resources ---
@router.post("/")
async def post_resource(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    body = await request.json()
    result = db.add_resource_asset(decoded.get("title", ""), body)
    return JSONResponse(status_code=result, content="Resource Added" if result == 200 else "Error Adding Resource")


# --- PUT /resources/{id} ---
@router.put("/{id}")
async def update_resource(request: Request, id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    body = await request.json()
    body["asset_id"] = id

    result = db.update_resource(decoded.get("title", ""), body)
    if result == 200:
        return JSONResponse(content={"message": f"Resource {id} updated successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=400, detail="Database update failed")

# --- DELETE /resources/{id} ---
@router.delete("/{id}")
async def delete_resource(request: Request, id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded = auth_result["decoded_payload"]
    await authorize_request(request, decoded)

    # Expect the DB layer to return something like {"deleted": 1}
    result = db.delete_resource(decoded.get("title", ""), id)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
