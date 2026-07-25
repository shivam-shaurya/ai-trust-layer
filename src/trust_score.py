"""Composite Trust Score: fuses the five trust signals into a single 0-100 score,
generates plain-language recommendations, and prepares radar chart data.

Weighting and thresholds are locked design decisions (see project memory / conversation):
equal 20% weight per signal (renormalized over whatever signals are currently available),
with score bands >=75 High Trust, 50-74 Moderate, <50 Low/Flagged.
"""

SIGNAL_WEIGHTS = {
    "prompt_safety": 0.2,
    "retrieval_quality": 0.2,
    "citation_coverage": 0.2,
    "semantic_consistency": 0.2,
    "hallucination_verification": 0.2,
}

# Signals not yet implemented (Milestone 3) are represented as None throughout this module.
PENDING_SIGNALS = {"citation_coverage", "semantic_consistency", "hallucination_verification"}

HIGH_TRUST_THRESHOLD = 75
MODERATE_TRUST_THRESHOLD = 50


def compute_trust_score(signals):
    """Combine available 0-1 signals into a 0-100 Trust Score.

    `signals` is a dict subset of SIGNAL_WEIGHTS' keys -> float in [0,1], or None for a
    signal that hasn't been computed yet. Weights for missing signals are dropped and the
    remaining weights are renormalized so they still sum to 1.
    """
    available = {k: v for k, v in signals.items() if v is not None}
    if not available:
        return 0.0

    total_weight = sum(SIGNAL_WEIGHTS[k] for k in available)
    weighted_sum = sum(SIGNAL_WEIGHTS[k] * available[k] for k in available)
    score = (weighted_sum / total_weight) * 100
    return round(max(0.0, min(100.0, score)), 1)


def trust_level(score):
    """Map a 0-100 Trust Score to a High/Moderate/Low label."""
    if score >= HIGH_TRUST_THRESHOLD:
        return "High Trust"
    if score >= MODERATE_TRUST_THRESHOLD:
        return "Moderate Trust"
    return "Low Trust"


def generate_recommendations(prompt_risk, retrieval_quality):
    """Generate plain-language recommendations from the prompt risk and retrieval quality
    results. Returns a list of strings; empty list means no concerns were raised.
    """
    recommendations = []

    if prompt_risk["category"] == "adversarial" or prompt_risk["risk_score"] >= 0.7:
        recommendations.append(
            "Prompt appears adversarial or high-risk. Review the query before trusting this answer."
        )
    elif prompt_risk["category"] == "out_of_domain":
        recommendations.append(
            "Question may be out-of-domain for the current document corpus."
        )
    elif prompt_risk["category"] == "ambiguous" or prompt_risk["risk_score"] >= 0.3:
        recommendations.append(
            "Question is ambiguous. Consider rephrasing for a more precise answer."
        )

    if retrieval_quality["score"] < 0.35:
        recommendations.append(
            "Low retrieval quality. Consider uploading more relevant documents."
        )
    elif retrieval_quality["distinct_sources"] <= 1 and retrieval_quality["diversity"] < 0.15:
        recommendations.append(
            "Evidence drawn from a single, narrow source. Consider diversifying the corpus."
        )

    if not recommendations:
        recommendations.append("Response verified: prompt is benign and evidence is well-matched.")

    return recommendations


def radar_chart_data(signals):
    """Prepare five-axis radar chart data. Pending (None) signals are rendered at a neutral
    0.5 placeholder value and flagged in `pending` so the UI can style/label them distinctly.

    Returns {"categories": [...], "values": [...], "pending": [bool, ...]}.
    """
    labels = {
        "prompt_safety": "Prompt Safety",
        "retrieval_quality": "Retrieval Quality",
        "citation_coverage": "Citation Coverage",
        "semantic_consistency": "Semantic Consistency",
        "hallucination_verification": "Hallucination Verification",
    }

    categories = []
    values = []
    pending = []
    for key, label in labels.items():
        categories.append(label)
        value = signals.get(key)
        if value is None:
            values.append(0.5)
            pending.append(True)
        else:
            values.append(value)
            pending.append(False)

    return {"categories": categories, "values": values, "pending": pending}
