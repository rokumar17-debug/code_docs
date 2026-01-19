# ---------------------------------------------------------
# backend/app/api/control.py (PAUSE / RESUME)
# ---------------------------------------------------------
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.state_manager import update_state


router = APIRouter(prefix="/control", tags=["Control"])




@router.post("/pause/{project_id}")
def pause(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    update_state(db, project_id, paused=True)
    return {"status": "paused"}




@router.post("/resume/{project_id}")
def resume(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    update_state(db, project_id, paused=False)
    return {"status": "resumed"}