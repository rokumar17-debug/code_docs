# backend/app/api/analysis.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.analysis_state import AnalysisState
from app.core.security import get_current_user

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/pause/{project_id}")
def pause_analysis(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    state = db.query(AnalysisState).filter_by(project_id=project_id).first()
    if not state:
        return {"status": "not_started"}

    state.paused = True
    db.commit()
    return {"status": "paused"}


@router.post("/resume/{project_id}")
def resume_analysis(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    state = db.query(AnalysisState).filter_by(project_id=project_id).first()
    if not state:
        return {"status": "not_started"}

    state.paused = False
    db.commit()
    return {"status": "resumed"}
