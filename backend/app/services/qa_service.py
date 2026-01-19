

# ---------------------------------------------------------
# backend/app/services/qa_service.py
# ---------------------------------------------------------


def answer_question(question: str, state: dict, persona: str):
    if "auth" in question.lower():
        return "Authentication is implemented using JWT with OAuth2 Bearer tokens."
    if persona == "PM":
        return "This feature enables secure access to the platform."
    return "Refer to architecture and API sections for details."