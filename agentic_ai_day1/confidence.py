def calculate_confidence(data):
    score = 100

    if not data["symptoms"]:
        score -= 25
    if not data["duration"]:
        score -= 25
    if not data["risk_flags"]:
        score -= 25

    return max(score, 0)