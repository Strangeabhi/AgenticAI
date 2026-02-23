import json
from ai_utils import call_ai

def classify_ticket(ticket_text):

    prompt = f"""
    You are a support AI system.

    Classify the ticket into:
    - category (Billing, Technical, Account, Other)
    - urgency (Low, Medium, High)
    - sentiment (Positive, Neutral, Negative)

    Return strictly valid JSON.
    No explanation.

    Ticket:
    {ticket_text}
    """

    response = call_ai(prompt)

    print("\n--- RAW AI RESPONSE ---")
    print(response)

    try:
        data = json.loads(response)
        return validate_ticket(data)
    except:
        return "❌ Invalid JSON returned."


def validate_ticket(data):

    allowed_categories = ["Billing", "Technical", "Account", "Other"]
    allowed_urgency = ["Low", "Medium", "High"]

    if data["category"] not in allowed_categories:
        return "❌ Invalid category"

    if data["urgency"] not in allowed_urgency:
        return "❌ Invalid urgency level"

    return data


if __name__ == "__main__":
    ticket = input("Enter support ticket:\n")
    result = classify_ticket(ticket)
    print("\n--- FINAL CLASSIFICATION ---\n")
    print(result)