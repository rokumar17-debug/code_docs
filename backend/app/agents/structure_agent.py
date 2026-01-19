# ---------------------------------------------------------
# backend/app/agents/structure_agent.py
# ---------------------------------------------------------
from app.services.preprocessing import preprocess_repository




def structure_agent(state: dict):
    repo_path = state["repo_path"]
    result = preprocess_repository(repo_path)
    state["structure"] = result
    return state