"""
Financial Risk Explanation Tool — Streamlit UI.
Run: streamlit run app.py
"""

import streamlit as st
from main import run

st.set_page_config(page_title="Financial Risk Explainer", page_icon="📊", layout="centered")

st.title("📊 Financial Risk Explanation Tool")
st.caption("Educational only — no investment advice")

st.markdown("""
**I can explain:** risk types, diversification, how mutual funds work.  
**I cannot:** recommend stocks or suggest exact investments.
""")

user_question = st.text_area(
    "Your question",
    placeholder="e.g. Explain diversification in mutual funds",
    height=100,
)

if st.button("Get explanation"):
    if not user_question or not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Getting answer..."):
            result = run(user_question.strip())
        if result.get("blocked"):
            st.error(result["with_disclaimer"])
        else:
            st.divider()
            st.markdown(result["with_disclaimer"])
