# ---------------------------------------------------------
# backend/app/services/doc_generator.py
# ---------------------------------------------------------
from typing import Dict




def generate_sde_report(state: Dict) -> Dict:
    return {
        "title": "Software Engineer Documentation",
        "sections": {
        "Architecture": "FastAPI-based backend with modular services and JWT auth.",
        "Code Structure": state.get("structure"),
        "API Overview": state.get("api"),
        "Setup": "pip install -r requirements.txt && uvicorn app.main:app",
        "Security": "JWT authentication with role-based access",
        }
    }




def generate_pm_report(state: Dict) -> Dict:
    return {
        "title": "Product Manager Documentation",
        "sections": {
        "Feature Inventory": state.get("pm_summary", {}).get("features"),
        "User Flow": "User uploads repo → analysis → documentation",
        "Limitations": state.get("pm_summary", {}).get("limitations"),
        "Roadmap": "Add semantic search and integrations",
        }
    }