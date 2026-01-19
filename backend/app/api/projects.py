
# from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, Form
# from sqlalchemy.orm import Session
# import zipfile, os

# from app.core.database import get_db, SessionLocal
# from app.core.security import get_current_user
# from app.models.project import Project
# from app.services.langgraph_runner import run_langgraph, run_langgraph_background

# router = APIRouter(prefix="/projects", tags=["Projects"])
# UPLOAD_DIR = "uploads"


# @router.post("/")
# def create_project(
#     name: str = Form(...),
#     persona: str = Form(...),
#     file: UploadFile = File(...),
#     background_tasks: BackgroundTasks = Depends(),
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user),
# ):
#     # 1️⃣ Create project
#     project = Project(
#         name=name,
#         persona=persona,
#         owner_id=user.id,
#         status="RUNNING"
#     )
#     db.add(project)
#     db.commit()
#     db.refresh(project)

#     # 2️⃣ Save zip
#     project_path = os.path.join(UPLOAD_DIR, str(project.id))
#     os.makedirs(project_path, exist_ok=True)

#     zip_path = os.path.join(project_path, file.filename)
#     with open(zip_path, "wb") as f:
#         f.write(file.file.read())

#     # 3️⃣ Extract zip
#     with zipfile.ZipFile(zip_path, "r") as zip_ref:
#         zip_ref.extractall(project_path)

#     # 4️⃣ Run LangGraph safely (new DB session)
#     background_tasks.add_task(
#         run_langgraph_background,
#         project.id,
#         project_path
#     )

#     return {
#         "project_id": project.id,
#         "status": "analysis started",
#         "progress_endpoint": f"/progress/{project.id}"
#     }

# backend/app/api/projects.py

from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, Form
from sqlalchemy.orm import Session
import zipfile, os

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.project import Project
from app.services.langgraph_runner import run_langgraph_background

router = APIRouter(prefix="/projects", tags=["Projects"])
UPLOAD_DIR = "uploads"


@router.post("/")
def create_project(background_tasks: BackgroundTasks,
    name: str = Form(...),
    persona: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    project = Project(
        name=name,
        persona=persona,
        owner_id=user.id,
        status="RUNNING"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    project_path = os.path.join(UPLOAD_DIR, str(project.id))
    os.makedirs(project_path, exist_ok=True)

    zip_path = os.path.join(project_path, file.filename)
    with open(zip_path, "wb") as f:
        f.write(file.file.read())

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(project_path)

    background_tasks.add_task(
        run_langgraph_background,
        project.id,
        project_path
    )

    return {
        "project_id": project.id,
        "status": "analysis started",
        "progress_endpoint": f"/progress/{project.id}"
    }


