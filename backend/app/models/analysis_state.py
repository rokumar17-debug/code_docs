# backend/app/models/analysis_state.py
from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean
from app.core.database import Base

class AnalysisState(Base):
    __tablename__ = "analysis_states"

    id = Column(BigInteger, primary_key=True)
    project_id = Column(
        BigInteger,
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True
    )
    stage = Column(String(50))
    message = Column(String)
    progress = Column(BigInteger, default=0)
    paused = Column(Boolean, default=False)
