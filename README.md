# TrustShield AI

A Trust Layer that wraps a RAG pipeline with a verification and explainability layer,
surfaced through a live Streamlit dashboard. Goal: score and explain how trustworthy each
answer is, not just generate fluent text.

## Status

**Milestone 2.5 (this commit):** basic RAG pipeline (ingestion, retrieval, generation) plus
a hybrid Prompt Risk Score (regex + embedding similarity + LLM reasoning), Retrieval
Quality scoring, a composite Trust Score with recommendations, and a five-axis trust radar
chart, surfaced in a Streamlit dashboard. Citation coverage, semantic consistency, and
hallucination verification (the remaining two radar axes) come in Milestone 3.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env
# edit .env and set OPENROUTER_API_KEY=sk-or-...
```

Get an OpenRouter API key at https://openrouter.ai/keys.

## Run

```bash
streamlit run app.py
```

On first query, the app builds a FAISS index from the `.txt` files in `docs/` (cached under
`index/`). Add your own source documents to `docs/` and delete the `index/` folder to
rebuild.

## Project layout

```
trustshield-ai/
├── app.py                  # Streamlit dashboard entrypoint
├── docs/                   # Source documents for the RAG corpus
├── index/                  # Generated FAISS index + chunk metadata (gitignored)
├── src/
│   ├── embeddings.py         # Shared sentence-transformers model, loaded once
│   ├── ingestion.py          # Load, chunk, embed, index documents
│   ├── retrieval.py          # Query FAISS index, return top-k chunks + scores + retrieval quality
│   ├── generation.py         # Call OpenRouter with retrieved context
│   ├── risk_scoring.py       # Hybrid Prompt Risk Score (regex + embedding + LLM)
│   ├── trust_score.py        # Composite Trust Score, recommendations, radar chart data
│   └── pipeline.py           # Orchestrates the full flow, records per-stage timing
├── eval/                   # Test questions + evaluation script (later milestone)
├── .env.example
└── requirements.txt
```

## Manual smoke test (no UI)

```bash
python -m src.pipeline
```

This runs one hardcoded question through risk scoring + retrieval + generation and prints
the answer, trust signals, and per-stage timings.
