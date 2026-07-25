"""Orchestrates the end-to-end RAG + trust-signal flow and records per-stage timing."""

import time

from src.generation import DEFAULT_MODEL, generate_answer
from src.retrieval import retrieve, score_retrieval_quality
from src.risk_scoring import score_prompt_risk


def run_pipeline(question, k=5, model=DEFAULT_MODEL):
    """Run risk scoring + retrieval + generation for `question`, returning the answer,
    retrieved chunks, prompt risk, retrieval quality, and a dict of stage -> elapsed seconds.
    """
    timings = {}

    t0 = time.perf_counter()
    prompt_risk = score_prompt_risk(question, model=model)
    timings["risk_scoring"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    chunks = retrieve(question, k=k)
    retrieval_quality = score_retrieval_quality(chunks, k_requested=k)
    timings["retrieval"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    answer = generate_answer(question, chunks, model=model)
    timings["generation"] = time.perf_counter() - t0

    timings["total"] = sum(timings.values())

    return {
        "question": question,
        "answer": answer,
        "chunks": chunks,
        "prompt_risk": prompt_risk,
        "retrieval_quality": retrieval_quality,
        "timings": timings,
    }


if __name__ == "__main__":
    result = run_pipeline("What is RAG and why does it help with hallucination?")
    print("Answer:\n", result["answer"])
    print("\nTimings:", result["timings"])
