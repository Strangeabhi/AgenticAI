import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from prompt_engine import build_prompt
from schema_validator import validate_schema
from risk_safety_engine import apply_risk_rules, build_safe_response
from state_manager import ConversationState


load_dotenv()

st.set_page_config(page_title="Supportive Mental Wellness Bot", layout="centered")

st.title("🌱 Mental Wellness Support (Educational Mode)")
st.write(
    "This is an **educational** demo that classifies student messages for emotional "
    "indicators and potential risk. It does **not** provide therapy, medical advice, "
    "or crisis counseling."
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
state = ConversationState()


def call_llm(user_input: str) -> str:

    prompt = build_prompt(user_input)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return completion.choices[0].message.content


user_input = st.text_area("Enter the student's message", height=160)

if st.button("Analyze Message"):

    if not user_input.strip():
        st.error("Input cannot be empty.")

    else:
        raw_response = call_llm(user_input)

        is_valid, data = validate_schema(raw_response)

        if not is_valid:
            st.error(f"Schema validation failed: {data}")
            st.write("Raw Model Output:")
            st.code(raw_response)

        else:
            rules_ok, updated_data, rules_message = apply_risk_rules(
                data, user_input
            )

            if not rules_ok:
                st.error(f"Guardrail failure: {rules_message}")
                st.json(updated_data)
            else:
                state.update(updated_data)

                if updated_data.get("blocked_instructions"):
                    st.error(
                        "I can’t help with instructions or steps for harming yourself or "
                        "someone else. Your safety matters a lot."
                    )

                if state.needs_clarification():
                    st.warning(
                        "The model was not confident about some fields: "
                        f"{state.missing_fields}"
                    )

                safe_response = build_safe_response(updated_data)

                st.subheader("Safe Educational Response")
                st.write(safe_response)

                st.subheader("Structured Classification Output")
                st.json(updated_data)

