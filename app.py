"""Streamlit dashboard entrypoint for the AI Trust Layer RAG pipeline (Milestone 2)."""

import streamlit as st

from src.pipeline import run_pipeline

st.set_page_config(page_title="AI Trust Layer", layout="wide")

st.title("AI Trust Layer")
st.caption("RAG pipeline with verification and explainability (Milestone 2: risk + retrieval quality)")


def risk_badge(risk_score, category):
    if risk_score >= 0.7:
        color = "red"
    elif risk_score >= 0.3:
        color = "orange"
    else:
        color = "green"
    st.markdown(
        f":{color}[**Prompt Risk: {risk_score:.2f} ({category})**]"
    )


def quality_badge(score):
    if score >= 0.6:
        color = "green"
    elif score >= 0.35:
        color = "orange"
    else:
        color = "red"
    st.markdown(f":{color}[**Retrieval Quality: {score:.2f}**]")


question = st.text_input("Ask a question about the documents in docs/")
ask_clicked = st.button("Ask")

if ask_clicked and question.strip():
    with st.spinner("Scoring prompt risk, retrieving context, and generating answer..."):
        try:
            result = run_pipeline(question)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    left, right = st.columns(2)

    with left:
        st.subheader("Answer")
        st.write(result["answer"])

        risk = result["prompt_risk"]
        risk_badge(risk["risk_score"], risk["category"])
        st.caption(risk["reason"])
        with st.expander("Prompt risk signal breakdown"):
            st.json(risk["signals"])

    with right:
        st.subheader("Retrieved Evidence")
        quality = result["retrieval_quality"]
        quality_badge(quality["score"])
        with st.expander("Retrieval quality breakdown"):
            st.json(quality)

        for chunk in result["chunks"]:
            with st.expander(
                f"{chunk['source']} #{chunk['chunk_id']} — similarity {chunk['score']:.3f}"
            ):
                st.write(chunk["text"])

    st.subheader("Timing")
    st.json(result["timings"])
elif ask_clicked:
    st.warning("Please enter a question.")
