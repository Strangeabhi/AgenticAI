from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root (one level above this file's directory)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

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