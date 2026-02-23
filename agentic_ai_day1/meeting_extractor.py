import json
from ai_utils import call_ai

def extract_meeting_data(text):

    prompt = f"""
    You are a corporate assistant.

    Extract:
    - meeting_summary (short paragraph)
    - decisions (list)
    - action_items (list of objects with task, owner, deadline)

    Return STRICT JSON only.
    No extra text.

    Meeting Notes:
    {text}
    """

    response = call_ai(prompt)

    print("\n--- RAW AI RESPONSE ---")
    print(response)

    try:
        data = json.loads(response)
        return validate_meeting(data)
    except:
        return "❌ AI returned invalid JSON."


def validate_meeting(data):

    if "action_items" not in data:
        return "❌ Missing action_items"

    for item in data["action_items"]:
        if not all(key in item for key in ["task", "owner", "deadline"]):
            return "❌ Invalid action item structure"

    return data


if __name__ == "__main__":
    notes = input("Paste meeting transcript:\n")
    result = extract_meeting_data(notes)
    print("\n--- STRUCTURED OUTPUT ---\n")
    print(result)