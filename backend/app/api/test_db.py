from app.core.database import engine

with engine.connect() as conn:
    print("DB connected successfully")
