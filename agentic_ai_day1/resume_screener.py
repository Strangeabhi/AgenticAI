import json
from ai_utils import call_ai

def screen_resume(resume_text):

    prompt = f"""
    You are an HR AI assistant.

    Extract the following from the resume:
    - candidate_name
    - skills (list)
    - years_experience (number)
    - suggested_role
    - suitability_score (0-10)

    Return STRICTLY valid JSON only.
    No explanation.

    Resume:
    {resume_text}
    """

    response = call_ai(prompt)

    print("\n--- RAW AI RESPONSE ---")
    print(response)

    try:
        data = json.loads(response)
        return validate_resume(data)
    except:
        return "❌ Invalid JSON returned by AI."


def validate_resume(data):

    required_fields = [
        "candidate_name",
        "skills",
        "years_experience",
        "suggested_role",
        "suitability_score"
    ]

    for field in required_fields:
        if field not in data:
            return f"❌ Missing field: {field}"

    if not isinstance(data["skills"], list):
        return "❌ Skills must be a list"

    if not isinstance(data["years_experience"], (int, float)):
        return "❌ Experience must be number"

    if not (0 <= data["suitability_score"] <= 10):
        return "❌ Score must be between 0 and 10"

    return data


if __name__ == "__main__":
    resume = input("Paste resume text:\n")
    result = screen_resume(resume)
    print("\n--- FINAL OUTPUT ---\n")
    print(result)