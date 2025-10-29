from src.app_factory import create_app
from src.DatabaseController.engine import connect_with_connector
import sqlalchemy

app = create_app()

# Optional sample route that uses the engine (kept for parity with your tests)
@app.get("/employees/count")
def employees_count():
    engine = connect_with_connector()
    with engine.connect() as conn:
        rows = conn.execute(sqlalchemy.text("SELECT 1")).fetchall()
    from src.logger import logger
    logger.security("employees_count accessed", level="info")
    return {"count": len(rows)}

if __name__ == "__main__":
    # simple manual poke if you run `python -m src.main`
    engine = connect_with_connector()
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM Employee"))
        for row in result:
            print(row)