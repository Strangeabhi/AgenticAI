from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from groq import Groq

from models import ReviewResponse, StandardsChunk
from prompts import build_system_prompt, build_user_prompt


# Load .env from the Review directory (next to this file), if present.
_CURRENT_DIR = Path(__file__).resolve().parent
_ENV_PATH = _CURRENT_DIR / ".env"
if _ENV_PATH.exists():
    load_dotenv(dotenv_path=str(_ENV_PATH))


GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=api_key)


def generate_review_with_llm(
    language: str,
    code: str,
    context: str | None,
    chunks: list[StandardsChunk],
) -> ReviewResponse:
    """
    Call Groq LLM with our system and user prompts and parse the JSON reply into a ReviewResponse.
    """
    client = _get_client()
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(language=language, code=code, context=context, chunks=chunks)

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    content = completion.choices[0].message.content or "{}"

    try:
        data: Dict[str, Any] = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model did not return valid JSON: {exc}\nRaw content: {content}") from exc

    return ReviewResponse.model_validate(data)

