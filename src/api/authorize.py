from fastapi import HTTPException, Request
from enum import Enum
from src.database.authorize import Role
from src.logger import logger

class EmployeeTitle(Enum):
    MANAGER = "manager"
    AIDE = "aide"
    DEVELOPER = "developer"
    SALESAGENT = "sales agent"

class ManagerTitle(Enum):
    MANAGER = "manager"

async def authorize_request(request: Request, decoded_payload: dict):
    """
    Determines access permissions based on employee title.
    Managers: allowed all actions.
    Others: allowed GET only.
    """
    user_title = decoded_payload.get("title", "").lower()
    method = request.method

    # Managers get full access
    if user_title in ManagerTitle.__members__:
        return {
            "authorized": True,
            "role": Role.MANAGER,
            "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
            "action": f"{method} request allowed"
        }

    # Non-managers can only query (GET)
    if method != "GET":
        raise HTTPException(status_code=403, detail="Only managers may modify resources")

    return {
        "authorized": True,
        "role": Role.EMPLOYEE,
        "allowed_methods": ["GET"],
        "action": f"{method} request allowed"
    }


def get_db_role(user_title: str = "") -> Role:
    """
    Returns the database role for the given user title.
    Args:
        user_title (str): The user's title.

    Returns:
        Role: The database role for the user.
    """
    logger.event(f"user_title: {user_title}", level="trace")

    user_title = user_title.lower()
    role = Role.OTHER
    if user_title == "manager":
        role = Role.MANAGER
    elif user_title == "aide":
        role = Role.AIDE
    elif user_title == "developer":
        role = Role.DEVELOPER
    elif user_title == "sales agent":
        role = Role.SALESAGENT



    return role
