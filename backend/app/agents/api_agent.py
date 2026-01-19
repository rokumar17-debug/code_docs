

# ---------------------------------------------------------
# backend/app/agents/api_agent.py
# ---------------------------------------------------------


def api_agent(state: dict):
    files = state["structure"]["files"]
    endpoints = [f for f in files if "api" in f.lower()]
    state["api"] = {"endpoints_detected": len(endpoints)}
    return state