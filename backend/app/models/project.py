# backend/app/models/project.py
from sqlalchemy import Column, BigInteger, String, ForeignKey
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    persona = Column(String(20), nullable=False)  # SDE / PM / BOTH
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(String(50), default="CREATED")
