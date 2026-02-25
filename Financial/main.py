"""
Financial Risk Explanation Tool.
CLI: python main.py
App: streamlit run app.py
"""

from config import RETRIES, DISCLAIMER
from intent_detector import detect_intent
from llm_engine import call_llm
from output_filter import filter_output


def run(user_question):
    """
    Full flow: intent check -> LLM -> output filter -> disclaimer.
    Returns dict with keys: with_disclaimer, blocked (None | "input" | "retries").
    """
    allowed, msg = detect_intent(user_question)
    if not allowed:
        return {"with_disclaimer": msg, "blocked": "input"}

    for attempt in range(RETRIES):
        raw = call_llm(user_question)
        if not raw:
            continue
        safe, filter_msg = filter_output(raw)
        if not safe:
            print("Output filter:", filter_msg)
            continue
        text = raw.strip() + "\n\n" + DISCLAIMER
        return {"with_disclaimer": text, "blocked": None}

    return {
        "with_disclaimer": "Unable to generate a safe explanation after retries.",
        "blocked": "retries",
    }


def main():
    print("Financial Risk Explanation Tool")
    print("I can explain: risk types, diversification, how mutual funds work.")
    print("I cannot: recommend stocks or suggest exact investments.\n")
    user_question = input("Your question: ").strip()
    if not user_question:
        print("No question entered.")
        return
    result = run(user_question)
    print("\n--- Response ---\n")
    print(result["with_disclaimer"])


if __name__ == "__main__":
    main()
