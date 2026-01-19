

# # ---------------------------------------------------------
# # backend/app/agents/pm_agent.py
# # ---------------------------------------------------------


# def pm_agent(state: dict):
#     state["pm_summary"] = {
#     "features": ["User Auth", "Project Analysis", "Live Progress"],
#     "limitations": ["No frontend auth yet"]
#     }
#     return state

# backend/app/agents/pm_agent.py

from typing import Dict, Any
from app.services.llm_service import run_llm


def pm_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    system = "You are a product manager explaining technical systems to business users."
    user = f"""
Code analysis summary:
{state}

Create a PM-friendly feature summary.
"""

    pm_summary = run_llm(system, user, temperature=0.4)

    state["pm_summary"] = pm_summary
    return state
