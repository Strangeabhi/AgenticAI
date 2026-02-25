from typing import Any, Dict, Tuple


def validate_budget(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Business rule validation focused on budget / price_range.

    Expects a dict with:
      - price_range: { "min": number or null, "max": number or null }
    Returns:
      - (True, "OK") if valid
      - (False, "reason") if invalid
    """
    price = data.get("price_range", {})
    min_val = price.get("min")
    max_val = price.get("max")

    # Allow both None: means user hasn't given any budget yet.
    if min_val is None and max_val is None:
        return False, "price_range (at least min or max) is required."

    # Must be numbers or None
    for label, val in [("min", min_val), ("max", max_val)]:
        if val is not None and not isinstance(val, (int, float)):
            return False, f"price_range.{label} must be a number or null."
        if isinstance(val, (int, float)) and val <= 0:
            return False, f"price_range.{label} must be > 0."

    # If both present, ensure min <= max
    if isinstance(min_val, (int, float)) and isinstance(max_val, (int, float)):
        if min_val > max_val:
            return False, "price_range.min cannot be greater than price_range.max."

    return True, "OK"

