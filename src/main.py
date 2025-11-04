import sqlalchemy
from fastapi import FastAPI
from src.app_factory import create_app
from src.database.database_connector import get_db_connection
from src.logger import logger

from fastapi.middleware.cors import CORSMiddleware

app = create_app()

@app.get("/")
async def root():
    return {"message": "Team Blue API is live 🚀"}

# Optional sample route that uses the engine (kept for parity with your tests)
@app.get("/employees/count")
def employees_count():
    engine = get_db_connection()
    with engine.connect() as conn:
        rows = conn.execute(sqlalchemy.text("SELECT 1")).fetchall()
    logger.security("employees_count accessed", level="info")
    return {"count": len(rows)}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # simple manual poke if you run `python -m src.main`
    engine = get_db_connection()
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM Employee"))
        for row in result:
            print(row)
