from typing import Any, Dict, List, Set, Tuple
import random


HIGH_RISK_KEYWORDS: Set[str] = {
    "suicide",
    "kill myself",
    "end it all",
    "don't want to live",
    "dont want to live",
    "self-harm",
    "self harm",
    "cutting",
    "cut myself",
    "overdose",
    "hurt someone",
    "hurt them",
    "kill them",
    "shoot",
    "stab",
}

# Patterns that indicate the user is asking for "how to" or step‑by‑step
INSTRUCTIONAL_PATTERNS: List[str] = [
    "how to ",
    "how do i ",
    "steps to ",
    "step by step",
    "guide me to ",
    "tutorial on ",
]


def _detect_high_risk_in_text(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for phrase in HIGH_RISK_KEYWORDS:
        if phrase in text_lower:
            found.append(phrase)
    return found


def apply_risk_rules(
    data: Dict[str, Any], user_message: str
) -> Tuple[bool, Dict[str, Any], str]:
    """
    Enforce local risk keyword detection and escalation logic.

    - Re-detect high‑risk keywords from the raw user message
    - Merge with model-provided risk_keywords
    - Force escalation_required / urgency_level when needed
    """
    detected = _detect_high_risk_in_text(user_message)
    model_keywords = [str(k).lower() for k in data.get("risk_keywords", [])]

    merged_keywords = sorted(set(model_keywords) | set(detected))
    data["risk_keywords"] = merged_keywords

    urgency = str(data.get("urgency_level", "low")).lower()

    # Block if user is asking for instructions combined with high‑risk content
    text_lower = user_message.lower()
    asking_for_instructions = any(pat in text_lower for pat in INSTRUCTIONAL_PATTERNS)

    if detected and asking_for_instructions:
        data["escalation_required"] = True
        data["urgency_level"] = "imminent"
        data["blocked_instructions"] = True
        return (
            True,
            data,
            "High‑risk + instructional request detected: content blocked and escalated.",
        )

    if detected:
        # Any high‑risk phrase means escalation is required
        data["escalation_required"] = True

        # Ensure urgency is at least "high"
        if urgency not in {"high", "imminent"}:
            urgency = "high"
        data["urgency_level"] = urgency

        # If the model forgot to mark escalation, we still continue
        # but explain that guardrails elevated the case.
        return True, data, "High‑risk language detected: escalation enforced."

    # No high‑risk keywords found by local detector
    # We still trust the model's escalation flag, but no extra constraint.
    data["escalation_required"] = bool(data.get("escalation_required", False))
    return True, data, "No high‑risk language detected by local rules."


def build_safe_response(data: Dict[str, Any]) -> str:
    """
    Render a safe, non‑clinical response template that:
    - Acknowledges feelings in warm, human terms
    - Uses gentle, optimistic language to lighten the mood
    - Avoids giving therapy or medical instructions
    - Encourages reaching out to trusted adults / professionals
    - Adds neutral crisis guidance when escalation is required
    """
    # Clean up emotional indicators; filter out placeholders like "null"
    raw_emotional = data.get("emotional_indicators", []) or []
    emotional = []
    for x in raw_emotional:
        if x is None:
            continue
        s = str(x).strip()
        if not s:
            continue
        if s.lower() in {"null", "none", "unknown", "n/a", "na"}:
            continue
        emotional.append(s)
    urgency = str(data.get("urgency_level", "low")).lower()
    escalate = bool(data.get("escalation_required", False))

    # Build several safe, optimistic variants and pick one at random
    feeling_phrase = ", ".join(emotional[:3]) if emotional else ""

    base_disclaimer = (
        "I’m an educational tool and not a mental health professional, "
        "so I can’t provide therapy, medical advice, or crisis counseling. "
    )

    variants_low_med = []

    if feeling_phrase:
        variants_low_med.append(
            f"Thanks for sharing that with me. It really sounds like you might be feeling {feeling_phrase}, "
            "and that can be a lot to carry. Even when days feel heavy, they don’t stay the same forever. "
            "You don’t have to figure everything out in one go. "
            + base_disclaimer
            + "If you can, try reaching out to a trusted adult like a parent, guardian, teacher, or school counselor so you don’t have to hold this alone."
        )
        variants_low_med.append(
            f"I hear you, and feeling {feeling_phrase} can be really draining. "
            "It’s okay if you don’t feel okay right now. Little bits of support and small, kind moments can slowly make things feel lighter. "
            + base_disclaimer
            + "Talking with someone you trust about this—maybe a parent, guardian, teacher, or counselor—could give you some extra care and perspective."
        )
        variants_low_med.append(
            f"What you’re describing sounds really tough, especially if you’re feeling {feeling_phrase}. "
            "You deserve patience and kindness from yourself and others. Feelings can shift over time, even if that change is slow. "
            + base_disclaimer
            + "If you’re able, consider sharing how you feel with a trusted adult so you don’t have to carry it all by yourself."
        )
    else:
        variants_low_med.append(
            "Thanks for opening up. It sounds like you might be going through something that feels pretty heavy. "
            "Even if it doesn’t seem like it right now, it’s possible for things to soften and change over time. "
            + base_disclaimer
            + "Reaching out to a trusted adult—like a parent, guardian, teacher, or school counselor—can help you feel less alone in this."
        )
        variants_low_med.append(
            "I’m glad you shared what’s on your mind. When life feels overwhelming, it can be hard to see any brightness ahead, "
            "but small, steady bits of support can help. "
            + base_disclaimer
            + "You might find it comforting to talk with someone you trust, such as a parent, guardian, teacher, or school counselor."
        )
        variants_low_med.append(
            "It sounds like things have been a lot to handle lately. That’s a heavy load for one person. "
            "You don’t have to have all the answers or fix everything at once. "
            + base_disclaimer
            + "Sharing some of this with a trusted adult could make it feel a little less lonely."
        )

    crisis_suffix = (
        " If you are in immediate danger, thinking about harming yourself or someone else, "
        "or feel unable to stay safe, please contact your local emergency services or a crisis hotline "
        "available in your country right away."
    )

    if not escalate and urgency in {"low", "medium"}:
        return random.choice(variants_low_med)

    # For high / imminent or explicit escalation, reuse the same variants but always add crisis guidance
    return random.choice(variants_low_med) + crisis_suffix

