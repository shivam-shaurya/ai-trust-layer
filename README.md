# TrustShield AI

A Trust Layer that wraps a RAG pipeline with a verification and explainability layer,
surfaced through a full-stack dashboard (FastAPI backend + React frontend). Goal: score
and explain how trustworthy each answer is, not just generate fluent text.

## Status

**Milestone 2.5 (this commit):** basic RAG pipeline (ingestion, retrieval, generation) plus
a hybrid Prompt Risk Score (regex + embedding similarity + LLM reasoning), Retrieval
Quality scoring, a composite Trust Score with recommendations, and a five-axis trust radar
chart. Citation coverage, semantic consistency, and hallucination verification (the
remaining two radar axes) come in Milestone 3.

## Architecture

- **Backend** (`server.py`): a FastAPI app wrapping `src/pipeline.run_pipeline` as a single
  `POST /api/ask` JSON endpoint.
- **Frontend** (`frontend/`): a Vite + React single-page app that calls the backend and
  renders the answer, evidence panel, Trust Score gauge, radar chart, and recommendations.

## Setup

Backend:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env
# edit .env and set OPENROUTER_API_KEY=sk-or-...
```

Get an OpenRouter API key at https://openrouter.ai/keys.

Frontend:

```bash
cd frontend
npm install
```

## Run

Two processes, in separate terminals:

```bash
# Terminal 1: backend (from the project root)
uvicorn server:app --reload --port 8000

# Terminal 2: frontend
cd frontend
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api/*` requests to the FastAPI
backend on port 8000 (see `frontend/vite.config.js`).

On the first query, the backend builds a FAISS index from the `.txt` files in `docs/`
(cached under `index/`). Add your own source documents to `docs/` and delete the `index/`
folder to rebuild.

## Project layout

```
trustshield-ai/
├── server.py                # FastAPI backend entrypoint
├── frontend/                # Vite + React dashboard
│   └── src/
│       ├── App.jsx            # Main layout and state
│       ├── api.js             # fetch() wrapper for the backend API
│       └── components/        # RiskBadge, QualityBadge, EvidencePanel, TrustGauge,
│                               # TrustRadar, Recommendations, Timing
├── docs/                    # Source documents for the RAG corpus
├── index/                   # Generated FAISS index + chunk metadata (gitignored)
├── src/
│   ├── embeddings.py         # Shared sentence-transformers model, loaded once
│   ├── ingestion.py          # Load, chunk, embed, index documents
│   ├── retrieval.py          # Query FAISS index, return top-k chunks + scores + retrieval quality
│   ├── generation.py         # Call OpenRouter with retrieved context
│   ├── risk_scoring.py       # Hybrid Prompt Risk Score (regex + embedding + LLM)
│   ├── trust_score.py        # Composite Trust Score, recommendations, radar chart data
│   └── pipeline.py           # Orchestrates the full flow, records per-stage timing
├── eval/                    # Test questions + evaluation script (later milestone)
├── .env.example
└── requirements.txt
```

## Manual smoke test (no UI)

```bash
python -m src.pipeline
```

This runs one hardcoded question through risk scoring + retrieval + generation and prints
the answer, trust signals, and per-stage timings.
