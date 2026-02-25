"""
Rule-based output filtering: block investment advice in model responses.
"""

BLOCKED_PHRASES = [
    "you should invest in",
    "you should buy",
    "I recommend investing in",
    "I recommend buying",
    "invest in this",
    "buy this stock",
    "buy these shares",
    "specific stock",
    "exact investment",
    "put your money in",
    "allocate to",
    "ticker symbol",
    "ticker:",
    "stock symbol",
    "buy now",
    "sell now",
    "you must invest",
    "you ought to invest",
]


def filter_output(output_text):
    """
    Returns (safe: bool, message: str).
    If not safe, message explains what was blocked; otherwise message is "ok".
    """
    if not output_text:
        return False, "Empty output"
    lower = output_text.lower()
    for phrase in BLOCKED_PHRASES:
        if phrase.lower() in lower:
            return False, f"Blocked phrase detected: {phrase}"
    return True, "ok"
