import json

REQUIRED_FIELDS = [
    "symptoms",
    "duration",
    "risk_flags",
    "follow_up_required"
]

def parse_json(output):
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return None

def validate_schema(data):
    if not data:
        return False, "Invalid JSON format"

    for field in REQUIRED_FIELDS:
        if field not in data:
            return False, f"Missing field: {field}"

    if not isinstance(data["symptoms"], list):
        return False, "Symptoms must be a list"

    if not isinstance(data["risk_flags"], list):
        return False, "risk_flags must be a list"

    if not isinstance(data["follow_up_required"], bool):
        return False, "follow_up_required must be boolean"

    return True, "Valid"