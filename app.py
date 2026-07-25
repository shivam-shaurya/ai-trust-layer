"""Streamlit dashboard entrypoint for TrustShield AI (Milestone 2.5: composite Trust Score,
recommendations, and radar chart on top of prompt risk + retrieval quality).
"""

import plotly.graph_objects as go
import streamlit as st

from src.pipeline import run_pipeline

st.set_page_config(page_title="TrustShield AI", layout="wide")

st.title("TrustShield AI")
st.caption(
    "A hybrid trust layer for retrieval-augmented LLM answers — prompt risk, retrieval "
    "quality, and a composite Trust Score with explainable recommendations."
)


def risk_badge(risk_score, category):
    if risk_score >= 0.7:
        color = "red"
    elif risk_score >= 0.3:
        color = "orange"
    else:
        color = "green"
    st.markdown(f":{color}[**Prompt Risk: {risk_score:.2f} ({category})**]")


def quality_badge(score):
    if score >= 0.6:
        color = "green"
    elif score >= 0.35:
        color = "orange"
    else:
        color = "red"
    st.markdown(f":{color}[**Retrieval Quality: {score:.2f}**]")


def trust_score_gauge(score, level):
    color = {"High Trust": "green", "Moderate Trust": "orange", "Low Trust": "red"}[level]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 100"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 50], "color": "#f8d7da"},
                    {"range": [50, 75], "color": "#fff3cd"},
                    {"range": [75, 100], "color": "#d4edda"},
                ],
            },
            title={"text": level},
        )
    )
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def trust_radar(radar):
    categories = radar["categories"] + [radar["categories"][0]]
    values = radar["values"] + [radar["values"][0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(r=values, theta=categories, fill="toself", name="Trust Signals")
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)
    if any(radar["pending"]):
        pending_labels = [c for c, p in zip(radar["categories"], radar["pending"]) if p]
        st.caption(
            f"Pending Milestone 3 (shown as neutral placeholders): {', '.join(pending_labels)}."
        )


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

    st.subheader("Trust Score")
    gauge_col, radar_col = st.columns(2)
    with gauge_col:
        trust_score_gauge(result["trust_score"], result["trust_level"])
    with radar_col:
        trust_radar(result["radar"])

    st.subheader("Recommendations")
    for rec in result["recommendations"]:
        st.markdown(f"- {rec}")

    st.subheader("Timing")
    st.json(result["timings"])
elif ask_clicked:
    st.warning("Please enter a question.")
