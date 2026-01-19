
# ---------------------------------------------------------
# backend/app/api/admin.py (FULL ADMIN DASHBOARD)
# ---------------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.project import Project


router = APIRouter(prefix="/admin", tags=["Admin"])




@router.get("/users")
def list_users(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(User).all()




@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}




@router.get("/projects")
def list_projects(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(Project).all()




@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"status": "deleted"}




@router.get("/metrics")
def system_metrics(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return {
    "total_users": db.query(User).count(),
    "total_projects": db.query(Project).count(),
    "active_projects": db.query(Project).filter(Project.status == "RUNNING").count()
    }

