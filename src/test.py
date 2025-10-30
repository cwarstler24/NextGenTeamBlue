import os

import src.DatabaseController.Database as db
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
from fastapi import FastAPI, Request, HTTPException
from src.logger import logger # Logger() instance
from src.validate import validate_request
from src.authenticate import authorize_request

# --- add near the top ---
import time
from fastapi.responses import JSONResponse
from fastapi import status

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
    return result[1]


@app.get("/resourcetypes")
async def get_resource_types(request: Request):
    #auth ......

    result = db.GetResourceTypes()
    return result[1]

@app.post("/resources")
async def post_resources(request: Request):
    #auth ......
    title = "manager"

    result = db.AddResource(title, request.json())
    return result

@app.put("/resources/{id}")
async def put_resources(request: Request):

    #auth ......
    title = "manager"
    result = db.UpdateResource(title, request.json())
    return result

