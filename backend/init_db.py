# backend/init_db.py
from app.core.database import Base, engine
from app.models.user import User
from app.models.project import Project
from app.models.analysis_state import AnalysisState

Base.metadata.create_all(bind=engine)
print("Postgres tables created successfully")
