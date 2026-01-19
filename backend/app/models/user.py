# backend/app/models/user.py
from sqlalchemy import Column, BigInteger, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
