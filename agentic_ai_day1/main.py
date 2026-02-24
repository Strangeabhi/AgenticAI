from safe_engine import safe_call

def build_prompt(note):
    return f"""
Extract structured data from the clinical note.

Return JSON only with:
{{
    "symptoms": [],
    "duration": "",
    "risk_flags": [],
    "follow_up_required": true/false
}}

Rules:
- Do not provide diagnosis
- Do not invent medication names
- Leave missing fields empty
- No extra text outside JSON

Clinical Note:
{note}
"""

if __name__ == "__main__":
    note = input("Enter clinical note: ")
    prompt = build_prompt(note)
    result = safe_call(prompt)

    print("\nFinal Structured Output:")
    print(result)