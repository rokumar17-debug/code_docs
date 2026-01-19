# # ---------------------------------------------------------
# # backend/app/services/langgraph_runner.py
# # ---------------------------------------------------------
# import asyncio
# from sqlalchemy.orm import Session
# from app.graphs.analysis_graph import build_analysis_graph
# from app.services.state_manager import update_state
# from app.services.progress_manager import progress_manager




# graph = build_analysis_graph()


# from app.core.database import SessionLocal

# def run_langgraph_background(project_id: int, path: str):
#     db = SessionLocal()
#     try:
#         run_langgraph(project_id, path, db)
#     finally:
#         db.close()


# async def run_langgraph(project_id: int, repo_path: str, db: Session):
#     state = {"repo_path": repo_path}


#     for step, node in enumerate(graph.stream(state)):
#         current_state = node


#         update_state(
#         db,
#         project_id,
#         stage=list(node.keys())[0],
#         progress=(step + 1) * 30,
#         message=f"Running agent: {list(node.keys())[0]}"
#         )


#         await progress_manager.publish(project_id, {
#         "stage": list(node.keys())[0],
#         "progress": (step + 1) * 30
#         })


#         # Pause handling
#         from app.models.analysis_state import AnalysisState
#         s = db.query(AnalysisState).filter_by(project_id=project_id).first()
#         while s.paused:
#             await asyncio.sleep(1)
#             s = db.query(AnalysisState).filter_by(project_id=project_id).first()



# backend/app/services/langgraph_runner.py

# import asyncio
# from sqlalchemy.orm import Session

# from app.graphs.analysis_graph import build_analysis_graph
# from app.services.state_manager import update_state
# from app.services.progress_manager import progress_manager
# from app.core.database import SessionLocal
# from app.models.analysis_state import AnalysisState

# graph = build_analysis_graph()


# def run_langgraph_background(project_id: int, repo_path: str):
#     """
#     Entry point for FastAPI BackgroundTasks (SYNC).
#     """
#     asyncio.run(run_langgraph(project_id, repo_path))


# async def run_langgraph(project_id: int, repo_path: str):
#     """
#     Main async LangGraph execution.
#     """
#     db: Session = SessionLocal()
#     try:
#         state = {"repo_path": repo_path}

#         for step, node in enumerate(graph.stream(state)):
#             stage = list(node.keys())[0]
#             progress = min((step + 1) * 30, 95)

#             # Update DB state
#             update_state(
#                 db=db,
#                 project_id=project_id,
#                 stage=stage,
#                 progress=progress,
#                 message=f"Running agent: {stage}",
#             )

#             # Publish realtime progress
#             await progress_manager.publish(
#                 project_id,
#                 {
#                     "stage": stage,
#                     "progress": progress,
#                 },
#             )

#             # Pause handling
#             while True:
#                 db.expire_all()
#                 s = (
#                     db.query(AnalysisState)
#                     .filter(AnalysisState.project_id == project_id)
#                     .first()
#                 )
#                 if not s or not s.paused:
#                     break
#                 await asyncio.sleep(1)

#         # Mark completed
#         update_state(
#             db=db,
#             project_id=project_id,
#             stage="COMPLETED",
#             progress=100,
#             message="Analysis completed",
#         )

#         await progress_manager.publish(
#             project_id,
#             {
#                 "stage": "COMPLETED",
#                 "progress": 100,
#             },
#         )

#     except Exception as e:
#         update_state(
#             db=db,
#             project_id=project_id,
#             stage="FAILED",
#             progress=0,
#             message=str(e),
#         )
#         raise
#     finally:
#         db.close()


# backend/app/services/langgraph_runner.py

import asyncio
from sqlalchemy.orm import Session
from app.graphs.analysis_graph import build_analysis_graph
from app.services.state_manager import update_state
from app.services.progress_manager import progress_manager
from app.core.database import SessionLocal
from app.models.analysis_state import AnalysisState

graph = build_analysis_graph()


def run_langgraph_background(project_id: int, repo_path: str):
    """
    SAFE entrypoint for FastAPI BackgroundTasks
    """
    db = SessionLocal()
    try:
        asyncio.run(run_langgraph(project_id, repo_path, db))
    finally:
        db.close()


async def run_langgraph(project_id: int, repo_path: str, db: Session):
    state = {"repo_path": repo_path}

    for step, node in enumerate(graph.stream(state)):
        stage = list(node.keys())[0]

        update_state(
            db=db,
            project_id=project_id,
            stage=stage,
            progress=min((step + 1) * 20, 95),
            message=f"Running agent: {stage}"
        )

        await progress_manager.publish(project_id, {
            "stage": stage,
            "progress": min((step + 1) * 20, 95)
        })

        # ⏸ Pause handling
        while True:
            s = db.query(AnalysisState).filter_by(project_id=project_id).first()
            if not s or not s.paused:
                break
            await asyncio.sleep(1)

    update_state(
        db=db,
        project_id=project_id,
        stage="completed",
        progress=100,
        message="Analysis completed"
    )


