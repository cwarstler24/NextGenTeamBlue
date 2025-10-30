# src/API/assets.py
from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/assets", tags=["assets"])

class AssetCreate(BaseModel):
    type: str
    location: str

class AssetService:
    # TODO: inject repo when DB is ready
    def create(self, payload: dict) -> dict:
        return {"id": 1, **payload}

def get_service() -> AssetService:
    return AssetService()

@router.post("", status_code=201)
def create_asset(body: AssetCreate, svc: AssetService = Depends(get_service)):
    allowed = {"laptop", "monitor", "phone"}
    if body.type not in allowed:
        raise HTTPException(status_code=400, detail="unsupported type")
    return svc.create(body.model_dump())
