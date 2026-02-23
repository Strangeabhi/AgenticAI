from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file (agentic_ai_day1)
CURRENT_DIR = Path(__file__).resolve().parent
env_path = CURRENT_DIR / ".env"
load_dotenv(dotenv_path=str(env_path))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(f"GROQ_API_KEY is not set; expected it in {env_path}")

client = Groq(api_key=api_key)

def call_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content