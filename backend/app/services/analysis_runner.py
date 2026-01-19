

# ================================
# backend/app/services/analysis_runner.py
# ================================
import asyncio
from app.services.progress_manager import progress_manager




async def run_analysis(project_id: int):
    stages = [
    ("PREPROCESSING", "Scanning repository", 20),
    ("STRUCTURE", "Detecting project structure", 40),
    ("API_ANALYSIS", "Analyzing API endpoints", 60),
    ("DOC_GEN", "Generating documentation", 80),
    ("DONE", "Analysis complete", 100),
    ]


    for stage, msg, pct in stages:
        await progress_manager.publish(project_id, {"stage": stage,"message": msg,"progress": pct})
        await asyncio.sleep(2) # simulate work

