# backend/app/models/code_embedding.py
from sqlalchemy import Column, BigInteger, Text
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class CodeEmbedding(Base):
    __tablename__ = "code_embeddings"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, index=True)
    file_path = Column(Text, nullable=False)
    content = Column(Text)
    embedding = Column(Vector(1536))

