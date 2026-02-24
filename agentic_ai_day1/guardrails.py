BLOCKED_PHRASES = [
    "diagnosis",
    "you have",
    "this indicates"
]

def check_scope_violation(output_text):
    for phrase in BLOCKED_PHRASES:
        if phrase.lower() in output_text.lower():
            return False, f"Blocked phrase detected: {phrase}"
    return True, "Safe"