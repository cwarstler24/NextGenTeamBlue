import os
import time
import sqlalchemy
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.logger import logger  # Logger() instance
from src.validate import validate_request
from src.authenticate import authenticate_request
from src.authorize import authorize_request
import src.database.database_controller as db # teammate’s DB controller
from google.cloud.sql.connector import Connector, IPTypes
import pymysql

app = FastAPI(
    title="Team Blue Inventory Listener",
    description="Listens for GET, POST, PUT, DELETE requests, validates tokens, authenticates identity, authorizes role, and executes DB actions.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Listener active on localhost"}

# GET /resources
@app.get("/resources")
async def get_resources(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Step 1: Validate
    validation_result = await validate_request(request, token)

    # Step 2: Authenticate
    authentication_result = await authenticate_request(request, token)
    decoded_payload = authentication_result["decoded_payload"]

    # Step 3: Authorize
    await authorize_request(request, decoded_payload)

    # Step 4: DB call (team function)
    result = db.GetResources()

    logger.info(f"GET /resources successful for {decoded_payload.get('fName')} {decoded_payload.get('lName')}")
    return JSONResponse(content=result[1], status_code=status.HTTP_200_OK)

# GET /resourcetypes
@app.get("/resourcetypes")
async def get_resource_types(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    await authorize_request(request, auth_result["decoded_payload"])

    result = db.GetResourceTypes()
    logger.info("GET /resourcetypes executed successfully")
    return JSONResponse(content=result[1], status_code=status.HTTP_200_OK)

# POST /resources
@app.post("/resources")
async def post_resources(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded_payload = auth_result["decoded_payload"]
    await authorize_request(request, decoded_payload)

    body = await request.json()

    # title pulled from token payload
    title = decoded_payload.get("title", "").lower()

    result = db.AddResource(title, body)

    logger.info(f"POST /resources created by {decoded_payload.get('fName')} {decoded_payload.get('lName')}")
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)

# PUT /resources/{id}
@app.put("/resources/{id}")
async def put_resources(request: Request, id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded_payload = auth_result["decoded_payload"]
    await authorize_request(request, decoded_payload)

    body = await request.json()
    title = decoded_payload.get("title", "").lower()

    result = db.UpdateResource(title, id, body)

    logger.info(f"PUT /resources/{id} updated by {decoded_payload.get('fName')} {decoded_payload.get('lName')}")
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

# DELETE /resources/{id}
@app.delete("/resources/{id}")
async def delete_resources(request: Request, id: int):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    await validate_request(request, token)
    auth_result = await authenticate_request(request, token)
    decoded_payload = auth_result["decoded_payload"]
    await authorize_request(request, decoded_payload)

    title = decoded_payload.get("title", "").lower()

    result = db.DeleteResource(title, id)

    logger.info(f"DELETE /resources/{id} by {decoded_payload.get('fName')} {decoded_payload.get('lName')}")
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
