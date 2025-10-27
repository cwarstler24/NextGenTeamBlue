# src/main.py
from fastapi import FastAPI, Request, HTTPException
from src.validate import validate_request

app = FastAPI(
    title="Team Blue Inventory Listener",
    description="Listens for GET, POST, PUT, DELETE requests and validates tokens.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Listener active on localhost"}

@app.api_route("/listener", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_request(request: Request):
    # Extract token from header
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Send the token & request data to validation.py
    validation_result = await validate_request(request, token)

    return {
        "method": request.method,
        "path": str(request.url),
        "validation_result": validation_result
    }
