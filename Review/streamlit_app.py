from __future__ import annotations

import json

import streamlit as st

from app_core import run_review
from models import ReviewRequest


st.set_page_config(page_title="CodeReview - RAG Code Review", layout="wide")

st.title("CodeSensei – RAG-Powered Code Review Mentor")
st.markdown(
    "Paste your code, pick a language, and CodeReview will review it **only** against the loaded coding standards. "
    "If no relevant rules exist, it will stay silent rather than guess."
)


with st.sidebar:
    st.header("Review Settings")
    language = st.selectbox(
        "Language",
        options=["python", "javascript", "typescript", "java", "go", "other"],
        index=0,
    )
    context = st.text_area(
        "Optional context (e.g. 'This is a REST controller for user management')",
        height=100,
    )


code = st.text_area("Code to review", height=320, placeholder="Paste your code here...")

col1, col2 = st.columns([1, 3])
with col1:
    run_button = st.button("Review Code", type="primary", use_container_width=True)


if run_button:
    if not code.strip():
        st.warning("Please paste some code first.")
    else:
        with st.spinner("Running CodeSensei review..."):
            request = ReviewRequest(language=language, code=code, context=context or None)
            try:
                response = run_review(request)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Review failed: {exc}")
            else:
                verdict_color = {
                    "approve": "green",
                    "approve_with_nits": "orange",
                    "request_changes": "red",
                    "no_coverage": "gray",
                }.get(response.verdict, "gray")

                st.markdown(f"**Verdict:** <span style='color:{verdict_color};'>{response.verdict}</span>", unsafe_allow_html=True)
                st.markdown(f"**Summary:** {response.summary}")

                st.subheader("Positive feedback")
                if not response.positive_feedback:
                    st.write("No explicit positives were identified from the standards corpus.")
                else:
                    for item in response.positive_feedback:
                        rules = ", ".join(item.rule_ids) if item.rule_ids else "—"
                        st.markdown(f"- {item.message} _(rules: {rules})_")

                st.subheader("Issues")
                if not response.issues:
                    st.write("No issues found (or no applicable standards).")
                else:
                    for issue in response.issues:
                        st.markdown(
                            f"**{issue.id}** – **{issue.severity.upper()}**  "
                            f"(rules: {', '.join(issue.rule_ids) if issue.rule_ids else '—'})"
                        )
                        st.write(issue.description)
                        if issue.affected_code:
                            with st.expander("Affected code"):
                                st.code(issue.affected_code, language=language)

                with st.expander("Raw response JSON"):
                    st.code(json.dumps(response.model_dump(), indent=2), language="json")

