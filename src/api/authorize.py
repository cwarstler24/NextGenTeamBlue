# src/autorize.py
from fastapi import HTTPException, Request

async def authorize_request(request: Request, decoded_payload: dict):
    """
    Determines access permissions based on employee title.
    Managers: allowed all actions.
    Others: allowed GET only.
    """
    user_title = decoded_payload.get("title", "").lower()
    method = request.method

    # Managers get full access
    if user_title == "manager":
        return {
            "authorized": True,
            "role": "Manager",
            "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
            "action": f"{method} request allowed"
        }

    # Non-managers can only query (GET)
    if method != "GET":
        raise HTTPException(status_code=403, detail="Only managers may modify resources")

    return {
        "authorized": True,
        "role": "Employee",
        "allowed_methods": ["GET"],
        "action": f"{method} request allowed"
    }
