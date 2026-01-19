# # backend/app/agents/web_search_agent.py

# from typing import Dict, Any


# def web_search_agent(state: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Adds best-practice recommendations based on detected stack.
#     (Web-augmented placeholder – safe for offline/local dev)
#     """

#     structure = state.get("structure", {})
#     db_info = state.get("db_analysis", {})

#     recommendations = []

#     # FastAPI
#     if "FastAPI" in str(structure):
#         recommendations.append(
#             "Follow FastAPI async endpoint patterns and dependency injection best practices."
#         )

#     # SQLAlchemy
#     if "SQLAlchemy" in db_info.get("orms", []):
#         recommendations.append(
#             "Use scoped sessions and avoid sharing DB sessions across async tasks."
#         )

#     # Security
#     recommendations.append(
#         "Follow OWASP Top 10 guidelines for authentication and authorization."
#     )

#     state["web_recommendations"] = {
#         "count": len(recommendations),
#         "items": recommendations,
#     }

#     return state

# backend/app/agents/web_search_agent.py

from typing import Dict, Any
from app.services.llm_service import run_llm


def web_search_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    stack = state.get("structure", {})
    db_info = state.get("db_analysis", {})

    system = "You are a senior software architect."
    user = f"""
Detected stack:
{stack}

Database info:
{db_info}

Give latest best practices and security recommendations.
"""

    recommendations = run_llm(system, user)

    state["web_recommendations"] = {
        "source": "openai",
        "content": recommendations
    }

    return state
