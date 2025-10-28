# src/main.py
from fastapi import FastAPI, Request, HTTPException
from src.validate import validate_request
from src.authenticate import authorize_request

app = FastAPI(
    title="Team Blue Inventory Listener",
    description="Listens for GET, POST, PUT, DELETE requests, validates tokens, and authorizes by role.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Listener active on localhost"}

@app.api_route("/listener", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_request(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Step 1: Validate token and request body
    validation_result = await validate_request(request, token)
    decoded_payload = validation_result["decoded_payload"]

    # Step 2: Authorize the request
    authorization_result = await authorize_request(request, decoded_payload)

    # Step 3: Return results
    return {
        "method": request.method,
        "path": str(request.url),
        "user": f"{decoded_payload.get('first_name', '')} {decoded_payload.get('last_name', '')}".strip(),
        "role": authorization_result["role"],
        "validation_result": validation_result,
        "authorization_result": authorization_result
    }
