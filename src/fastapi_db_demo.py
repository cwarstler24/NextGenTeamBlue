import os
from src.logger import logger

import src.database.database_controller as db
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
from fastapi import FastAPI, Request, HTTPException
from src.logger import logger # Logger() instance
from src.validate import validate_request
from src.authenticate import authorize_request

import logging

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger._logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_name == 'emit':
            frame = frame.f_back
            depth += 1
        logger._logger.bind(type="event").opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

logging.getLogger().addHandler(InterceptHandler())
logging.getLogger().setLevel("INFO")

# --- add near the top ---
import time
from datetime import date, datetime
from fastapi.responses import JSONResponse
from fastapi import status

def convert_bytes_to_strings(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [convert_bytes_to_strings(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_bytes_to_strings(value) for key, value in obj.items()}
    else:
        return obj

app = FastAPI(
    title="Team Blue Inventory Listener",
    description="Listens for GET, POST, PUT, DELETE requests, validates tokens, and authorizes by role.",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Listener active on localhost"}

@app.get("/resources")
async def get_resources(request: Request):
    #auth ......

    result = db.GetResources()
    logger.event(f"Result Code: {result[0]}", level="info")
    return JSONResponse(status_code=result[0], content=convert_bytes_to_strings(result[1]))



@app.get("/resourcetypes")
async def get_resource_types(request: Request):
    #auth ......

    result = db.GetResourceTypes()
    logger.event(f"Result Code: {result[0]}", level="info")
    return JSONResponse(status_code=result[0], content=convert_bytes_to_strings(result[1]))

@app.post("/resources")
async def post_resources(request: Request):
    #auth ......
    title = "Manager"

    result = db.AddResourceAsset(title, await request.json())
    logger.event(f"Result Code: {result}", level="info")
    if result == 200:
        return JSONResponse(status_code=result, content="Resource Added")
    else:
        return JSONResponse(status_code=result, content="Error Adding Resource")

@app.put("/resources/{id}")
async def put_resources(request: Request):

    #auth ......
    title = "manager"
    result = db.UpdateResource(title, request.json())
    return result

