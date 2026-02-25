"""
Detect user intent. Block "should I invest in X?" and other advice-seeking questions.
"""

import re

BLOCKED_INPUT_PATTERNS = [
    r"should\s+I\s+invest\s+in",
    r"can\s+I\s+invest\s+in\s+.+\?",
    r"is\s+\w+\s+a\s+good\s+investment\s*\??",
    r"which\s+(stock|fund|etf)\s+should\s+I\s+buy",
    r"recommend\s+(me\s+)?(a\s+)?(stock|fund|investment)",
    r"which\s+fund\s+should\s+I\s+choose",
]

# Substring block: if question contains any of these, block
BLOCKED_PHRASES = [
    "should i invest in",
    "best mutual fund to buy",
    "which fund should i choose",
]

# Block if question contains BOTH words (e.g. "recommend" and "stock")
BLOCKED_WORD_PAIRS = [
    ("recommend", "stock"),
    ("suggest", "investment"),
]

BLOCKED_MESSAGE = (
    "This tool only explains concepts (e.g. risk types, diversification). "
    "It cannot advise whether to invest in specific products."
)


def detect_intent(user_text):
    """
    Returns (allowed: bool, message: str).
    If not allowed, message is the block reason; otherwise message is "ok".
    """
    if not user_text or not user_text.strip():
        return False, "Empty input"
    lower = user_text.strip().lower()
    for pattern in BLOCKED_INPUT_PATTERNS:
        if re.search(pattern, user_text, re.IGNORECASE):
            return False, BLOCKED_MESSAGE
    for phrase in BLOCKED_PHRASES:
        if phrase in lower:
            return False, BLOCKED_MESSAGE
    for word1, word2 in BLOCKED_WORD_PAIRS:
        if word1 in lower and word2 in lower:
            return False, BLOCKED_MESSAGE
    return True, "ok"
