from fastapi import HTTPException, Request
from src.database.authorize import Role
from src.logger import logger


async def authorize_request(request: Request, decoded_payload: dict):
    """
    Determines access permissions based on employee title.
    Managers: allowed all actions.
    Others: allowed GET only.
    Args:
        request (Request): The request object.
        decoded_payload (dict). The
    """
    user_title = decoded_payload.get("title", "").lower()
    method = request.method

    # Managers get full access
    database_role = get_db_role(user_title)
    if database_role == Role.MANAGER:
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
    Managers get full access, all other roles (Developer, Aide, Sales Agent, etc.) get employee access.
    
    Args:
        user_title (str): The user's title.

    Returns:
        Role: The database role for the user.
    """
    logger.event(f"user_title: {user_title}", level="trace")

    user_title = user_title.lower()
    
    # Managers get manager role
    if user_title in ["manager", "admin", "administrator"]:
        return Role.MANAGER
    
    # All other roles (developer, aide, sales agent, etc.) get employee access
    if user_title in ["aide", "developer", "sales agent", "employee", "user"]:
        return Role.EMPLOYEE
    
    # Unknown roles default to OTHER (no access)
    return Role.OTHER
