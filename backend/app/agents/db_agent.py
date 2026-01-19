# backend/app/agents/db_agent.py

import os
import re
from typing import Dict, Any


def db_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes database usage and data models in the repository.
    """
    repo_path = state["repo_path"]

    db_info = {
        "orm": set(),
        "models": [],
        "files": [],
    }

    for root, _, files in os.walk(repo_path):
        for file in files:
            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)
            try:
                content = open(path, "r", encoding="utf-8").read()
            except Exception:
                continue

            # Detect ORM usage
            if "sqlalchemy" in content.lower():
                db_info["orm"].add("SQLAlchemy")
            if "django.db" in content.lower():
                db_info["orm"].add("Django ORM")

            # Detect models
            if re.search(r"class\s+\w+\(.*Base.*\)", content):
                db_info["models"].append(file)
                db_info["files"].append(path)

    state["db_analysis"] = {
        "orms": list(db_info["orm"]),
        "model_files": db_info["models"],
        "summary": f"Detected ORM(s): {', '.join(db_info['orm']) or 'None'}",
    }

    return state
