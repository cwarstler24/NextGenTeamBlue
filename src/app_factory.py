from fastapi import FastAPI
from src.API.assets import router as assets_router
from src.API.health import router as health_router
from src.API.listener import router as listener_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Team Blue Inventory Listener",
        description="Listens for GET, POST, PUT, DELETE requests, validates tokens, and authorizes by role.",
        version="1.0.0",
    )
    app.include_router(health_router)
    app.include_router(listener_router)
    app.include_router(assets_router)
    return app
