import sqlalchemy
from src.app_factory import create_app
from src.database.database_connector import get_db_connection
from src.logger import logger

app = create_app()

# Optional sample route that uses the engine (kept for parity with your tests)
@app.get("/employees/count")
def employees_count():
    with get_db_connection.connect() as conn:
        rows = conn.execute(sqlalchemy.text("SELECT 1")).fetchall()
    logger.security("employees_count accessed", level="info")
    return {"count": len(rows)}

if __name__ == "__main__":
    # simple manual poke if you run `python -m src.main`
    db_connector = get_db_connection()
    with db_connector.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM Employee"))
        for row in result:
            print(row)