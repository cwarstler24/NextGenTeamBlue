# src/API/assets.py
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from src.database import database_controller as db_ctrl
import src.database.authorize as auth

router = APIRouter(prefix="/assets", tags=["assets"])

class AssetCreate(BaseModel):
    type: str
    location: str

class AssetService:
    def create(self, payload: dict) -> dict:
        return {"id": 1, **payload}
    def list(self) -> list[dict]:
        # Fetch real assets from DB via controller
        # Use EMPLOYEE role for read access (OTHER has no access)
        status, items = db_ctrl.get_resources(user_position=auth.Role.EMPLOYEE)
        if status != 200:
            raise HTTPException(status_code=status, detail="Failed to fetch assets")
        return items
    def get_by_id(self, asset_id: int) -> dict:
        # Fetch single asset by ID
        status, item = db_ctrl.get_resource_by_id(asset_id, user_position=auth.Role.EMPLOYEE)
        if status == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if status != 200 or not item:
            raise HTTPException(status_code=404, detail="Asset not found")
        return item

def get_service() -> AssetService:
    return AssetService()

def require_bearer(request: Request):
    """Minimal bearer token guard: require Authorization: Bearer <token> header.
    Replace with full authenticate/authorize dependencies when available.
    """
    authorization = request.headers.get("authorization", "")
    
    # # Debug logging
    # print(f"Authorization header received: {authorization[:20] if authorization else 'None'}...")
    # print(f"Full header value: '{authorization}'")
    # print(f"Header length: {len(authorization)}")
    # print(f"Starts with 'bearer '? {authorization.lower().startswith('bearer ')}")
    # print(f"Starts with 'Bearer '? {authorization.startswith('Bearer ')}")
    
    if not authorization or not authorization.lower().startswith("bearer "):
        print(f"FAILED: authorization='{authorization}'")
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    print("PASSED bearer check")
    # Normalize: return exactly 'Bearer <token>'
    parts = authorization.split(" ", 1)
    token_value = parts[1].strip() if len(parts) > 1 else ""
    return f"Bearer {token_value}"

@router.post("", status_code=201)
def create_asset(body: AssetCreate, svc: AssetService = Depends(get_service), _auth: str = Depends(require_bearer)):
    allowed = {"laptop", "monitor", "phone"}
    if body.type not in allowed:
        raise HTTPException(status_code=400, detail="unsupported type")
    return svc.create(body.model_dump())

@router.get("")
def list_assets(svc: AssetService = Depends(get_service), _auth: str = Depends(require_bearer)):
    return svc.list()

@router.get("/{asset_id}")
def get_asset(asset_id: int, svc: AssetService = Depends(get_service), _auth: str = Depends(require_bearer)):
    return svc.get_by_id(asset_id)
