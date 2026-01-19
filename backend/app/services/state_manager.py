

# # ---------------------------------------------------------
# # backend/app/services/state_manager.py
# # ---------------------------------------------------------
# from sqlalchemy.orm import Session
# from app.models.analysis_state import AnalysisState




# def get_or_create_state(db: Session, project_id: int) -> AnalysisState:
#     state = db.query(AnalysisState).filter_by(project_id=project_id).first()
#     if not state:
#         state = AnalysisState(project_id=project_id, stage="INIT")
#         db.add(state)
#         db.commit()
#         db.refresh(state)
#     return state




# def update_state(db: Session, project_id: int, **kwargs):
#     state = get_or_create_state(db, project_id)
#     for k, v in kwargs.items():
#         setattr(state, k, v)
#     db.commit()


# backend/app/services/state_manager.py

from sqlalchemy.orm import Session
from app.models.analysis_state import AnalysisState

def update_state(
    db: Session,
    project_id: int,
    stage: str,
    progress: int,
    message: str,
):
    state = (
        db.query(AnalysisState)
        .filter(AnalysisState.project_id == project_id)
        .first()
    )

    if not state:
        state = AnalysisState(
            project_id=project_id,
            stage=stage,
            progress=progress,
            message=message,
        )
        db.add(state)
    else:
        state.stage = stage
        state.progress = progress
        state.message = message

    db.commit()
