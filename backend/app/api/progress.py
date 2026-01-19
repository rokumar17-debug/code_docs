# #===============================
# # backend/app/api/progress.py
# # ================================
# from fastapi import APIRouter, Depends
# from fastapi.responses import StreamingResponse
# import json


# from app.services.progress_manager import progress_manager
# from app.core.security import get_current_user
# from collections import defaultdict

# router = APIRouter(prefix="/progress", tags=["Progress"])




# @router.get("/{project_id}")
# async def stream_progress(project_id: int, user=Depends(get_current_user)):
#     queue = await progress_manager.subscribe(project_id)
#     async def event_generator():
#         while True:
#             data = await queue.get()
#             yield f"data: {json.dumps(data)}\n\n"


#     return StreamingResponse(event_generator(), media_type="text/event-stream")

# backend/app/api/progress.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.analysis_state import AnalysisState
from app.core.security import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/{project_id}")
def get_progress(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    state = (
        db.query(AnalysisState)
        .filter(AnalysisState.project_id == project_id)
        .first()
    )

    if not state:
        return {
            "stage": "initializing",
            "progress": 0,
            "message": "Starting analysis",
            "paused": False
        }

    return {
        "stage": state.stage,
        "progress": state.progress,
        "message": state.message,
        "paused": state.paused
    }
