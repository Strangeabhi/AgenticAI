import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

from prompt_engine import build_prompt
from schema_validator import validate_schema
from business_rules import validate_budget
from state_manager import ConversationState

load_dotenv()

st.set_page_config(page_title="Product Query Normalizer", layout="centered")

st.title("🛍️ Product Query Normalizer")
st.write("Structured parsing + ambiguity detection + guardrails")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
state = ConversationState()


def call_llm(user_input):

    prompt = build_prompt(user_input)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return completion.choices[0].message.content


user_input = st.text_input("Enter your shopping query")

if st.button("Normalize Query"):

    if not user_input.strip():
        st.error("Input cannot be empty.")

    else:
        response = call_llm(user_input)

        is_valid, data = validate_schema(response)

        if not is_valid:
            st.error(f"Schema validation failed: {data}")
            st.write("Raw Model Output:")
            st.code(response)

        else:
            budget_valid, message = validate_budget(data)

            if not budget_valid:
                st.error(f"Business rule failed: {message}")

            else:
                state.update(data)

                if state.needs_clarification():
                    st.warning(
                        f"Need clarification for: {state.missing_fields}"
                    )
                else:
                    st.success("Structured Output")
                    st.json(data)