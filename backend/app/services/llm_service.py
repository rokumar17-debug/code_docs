from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def run_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2
) -> str:
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content
