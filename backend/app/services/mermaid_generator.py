# ---------------------------------------------------------
# backend/app/services/mermaid_generator.py
# ---------------------------------------------------------


def architecture_diagram():
    return """
        ```mermaid
            graph TD
            User -->|Upload Repo| API[FastAPI]
            API --> LangGraph
            LangGraph --> Agents
            Agents --> Docs
            ```
        """




def api_sequence_diagram():
    return """
        ```mermaid
        sequenceDiagram
        User->>API: POST /projects
        API->>LangGraph: start analysis
        LangGraph-->>API: progress updates
        API-->>User: SSE events
        ```
    """