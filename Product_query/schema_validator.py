import json
from typing import Any, Dict, List, Tuple


def validate_schema(raw_json: str) -> Tuple[bool, Any]:
    """
    Basic schema validation that matches how app.py calls it.

    - Takes the LLM JSON string (raw_json)
    - Parses it into a Python dict
    - Ensures expected top-level keys exist with reasonable defaults
    - Returns:
        (True, data_dict)  on success
        (False, error_msg) on failure
    """
    try:
        data: Any = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        return False, f"Invalid JSON: {exc}"

    if not isinstance(data, dict):
        return False, "Top-level JSON must be an object."

    # Ensure required top-level keys exist (with defaults)
    data.setdefault("product_type", None)

    price = data.get("price_range")
    if not isinstance(price, dict):
        price = {}
    price.setdefault("min", None)
    price.setdefault("max", None)
    data["price_range"] = price

    data.setdefault("usage_context", None)

    feature_prefs = data.get("feature_preferences")
    if not isinstance(feature_prefs, list):
        feature_prefs = []
    data["feature_preferences"] = feature_prefs

    missing_fields = data.get("missing_fields")
    if not isinstance(missing_fields, list):
        missing_fields = []
    data["missing_fields"] = missing_fields

    return True, data