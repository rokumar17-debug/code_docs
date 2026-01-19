

# ================================
# backend/app/schemas/project.py
# ================================
from pydantic import BaseModel




class ProjectCreate(BaseModel):
    name: str
    persona: str # SDE / PM / BOTH