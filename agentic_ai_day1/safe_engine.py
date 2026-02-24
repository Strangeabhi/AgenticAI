from ai_wrapper import call_llm
from validator import parse_json, validate_schema
from guardrails import check_scope_violation
from confidence import calculate_confidence
from config import RETRIES

def safe_call(prompt):
    for attempt in range(RETRIES):
        print(f"Attempt {attempt+1}")
        raw_output = call_llm(prompt)

        if not raw_output:
            continue

        safe, message = check_scope_violation(raw_output)
        if not safe:
            print("Guardrail triggered:", message)
            continue

        parsed = parse_json(raw_output)
        valid, validation_msg = validate_schema(parsed)

        if valid:
            parsed["confidence_score"] = calculate_confidence(parsed)
            return parsed
        else:
            print("Validation failed:", validation_msg)

    return {"error": "Failed after retries"}
