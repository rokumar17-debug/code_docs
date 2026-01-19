

# ---------------------------------------------------------
# backend/app/api/docs.py
# ---------------------------------------------------------
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.doc_generator import generate_sde_report, generate_pm_report
from app.services.mermaid_generator import architecture_diagram, api_sequence_diagram
from app.services.qa_service import answer_question


router = APIRouter(prefix="/docs", tags=["Documentation"])


# NOTE: state would come from LangGraph persisted output
MOCK_STATE = {}




@router.get("/{project_id}/sde")
def get_sde_docs(project_id: int, user=Depends(get_current_user)):
    return {
    "report": generate_sde_report(MOCK_STATE),
    "diagrams": [architecture_diagram(), api_sequence_diagram()]
    }




@router.get("/{project_id}/pm")
def get_pm_docs(project_id: int, user=Depends(get_current_user)):
    return {
    "report": generate_pm_report(MOCK_STATE),
    "diagrams": [architecture_diagram()]
    }




@router.post("/{project_id}/qa")
def qa(project_id: int, question: str, persona: str, user=Depends(get_current_user)):
    return {
    "answer": answer_question(question, MOCK_STATE, persona)
    }

