# src/test.py
from fastapi import FastAPI
from src.api.routes import resources

app = FastAPI(
    title="Team Blue Inventory API",
    description="REST API for managing inventory assets with authentication and authorization.",
    version="1.0.0"
)

# Register route groups
app.include_router(resources.router)

@app.get("/")
async def root():
    return {"message": "Team Blue API is live 🚀"}
