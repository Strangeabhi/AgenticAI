import json
from typing import Any, Dict, List, Tuple


VALID_URGENCY = {"low", "medium", "high", "imminent"}


def _ensure_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def validate_schema(raw_json: str) -> Tuple[bool, Any]:
    """
    Parse and normalize the LLM JSON for the Supportive bot.

    Returns:
        (True, data_dict)  on success
        (False, error_msg) on failure
    """
    try:
        data: Any = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        return False, f"Invalid JSON: {exc}"

    if not isinstance(data, dict):
        return False, "Top-level JSON must be an object."

    # emotional_indicators: always a list of strings
    emotional = _ensure_list(data.get("emotional_indicators"))
    data["emotional_indicators"] = [str(x) for x in emotional if x is not None]

    # urgency_level: constrained string with fallback
    urgency = data.get("urgency_level")
    if not isinstance(urgency, str) or urgency.lower() not in VALID_URGENCY:
        urgency = "low"
    data["urgency_level"] = urgency.lower()

    # risk_keywords: list of strings
    rk = _ensure_list(data.get("risk_keywords"))
    data["risk_keywords"] = [str(x).lower() for x in rk if x is not None]

    # escalation_required: boolean
    esc = data.get("escalation_required")
    data["escalation_required"] = bool(esc)

    # notes_for_human_counselor: optional string
    notes = data.get("notes_for_human_counselor")
    if notes is not None:
        notes = str(notes)
    data["notes_for_human_counselor"] = notes

    # missing_fields: list of strings
    mf = _ensure_list(data.get("missing_fields"))
    data["missing_fields"] = [str(x) for x in mf if x is not None]

    return True, data

