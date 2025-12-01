from fastapi import FastAPI
from src.api.assets import router as assets_router
from src.api.health import router as health_router
from src.api.routes import resources
from src.api.pages import router as pages

def create_app() -> FastAPI:
    app = FastAPI(
        title="Team Blue Inventory Listener",
        description="Listens for GET, POST, PUT, DELETE requests" \
        ", validates tokens, and authorizes by role.",
        version="1.0.0",
    )
    app.include_router(health_router)
    app.include_router(assets_router)
    app.include_router(resources.router)
    app.include_router(pages)
    return app
