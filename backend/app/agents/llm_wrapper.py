# ---------------------------------------------------------
# backend/app/agents/llm_wrapper.py
# ---------------------------------------------------------
from app.core.observability import trace_llm_call




def call_llm(prompt: str, agent: str):
    with trace_llm_call(name=f"{agent}-llm-call",
    metadata={"agent": agent, "prompt_size": len(prompt)}
    ):
    # Placeholder for real LLM call (OpenAI/Claude)
        return f"LLM response for {agent}"