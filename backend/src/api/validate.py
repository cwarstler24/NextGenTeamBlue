from fastapi import HTTPException, Request
from src.security import data_validation
from src.logger import logger

async def validate_request(request: Request, token: str):
    """
    Validates an incoming API request.
    - Ensures token format is valid.
    - Validates body fields for POST and PUT requests.
    - Enforces XOR rule: exactly one of location_id or employee_id must be provided.
    Raises HTTPException on validation failure.
    """

    if not token or not token.startswith("Bearer "):
        logger.event("Invalid token", level="warning")
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # --- Step 2: For POST/PUT, validate JSON body against schema ---
    if request.method in ["POST", "PUT"]:
        logger.event("Validating request body", level="info")
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or missing JSON body")

        if not body:
            raise HTTPException(status_code=400, detail="Empty request body")

        is_valid = data_validation.data_validation(body)
        if not is_valid:
            logger.event("Data validation failed", level="warning")
            raise HTTPException(status_code=400, detail=
                                "Data validation failed: Invalid or missing JSON body")

    logger.event("Validation succeeded", level="info")
    return {
        "status": "valid",
        "method": request.method
    }
