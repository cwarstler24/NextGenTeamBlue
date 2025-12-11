from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.assets import router as assets_router
from src.api.health import router as health_router
from src.api.routes import resources
from src.api.routes.auth_proxy import router as auth_proxy_router
from src.api.pages import router as pages

def create_app() -> FastAPI:
    app = FastAPI(
        title="Team Blue Inventory Listener",
        description="Listens for GET, POST, PUT, DELETE requests" \
        ", validates tokens, and authorizes by role.",
        version="1.0.0",
    )
    
    # Add CORS middleware BEFORE including routes
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development only - restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(health_router)
    app.include_router(auth_proxy_router)
    app.include_router(assets_router)
    app.include_router(resources.router)
    app.include_router(pages)
    return app
