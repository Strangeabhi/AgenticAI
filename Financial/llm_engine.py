"""
LLM engine: load .env, Groq client, scope-restricted prompt, call_llm.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from config import MODEL_NAME, TEMPERATURE

CURRENT_DIR = Path(__file__).resolve().parent
env_path = CURRENT_DIR / ".env"
load_dotenv(dotenv_path=str(env_path))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(f"GROQ_API_KEY is not set; expected it in {env_path}")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """You are a financial education assistant. Your role is ONLY to explain concepts.

You MAY explain:
- Risk types (e.g. market risk, credit risk, liquidity risk)
- Diversification and how it works
- How mutual funds work in general
- Definitions and educational content

You must NOT:
- Recommend specific stocks, funds, or ETFs
- Suggest exact investments or allocations
- Tell the user what to buy or sell
- Give personal investment advice

Respond in clear, plain text. Keep answers focused and educational only."""


def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("API Error:", e)
        return None
