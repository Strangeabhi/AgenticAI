from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv
from config import MODEL_NAME, TEMPERATURE

CURRENT_DIR = Path(__file__).resolve().parent
env_path = CURRENT_DIR / ".env"
load_dotenv(dotenv_path=str(env_path))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(f"GROQ_API_KEY is not set; expected it in {env_path}")

client = Groq(api_key=api_key)


def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a clinical data extraction engine. Return valid JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("API Error:", e)
        return None