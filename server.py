"""FastAPI backend for TrustShield AI. Wraps src.pipeline.run_pipeline as a JSON API
consumed by the React frontend (frontend/)."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pipeline import run_pipeline

app = FastAPI(title="TrustShield AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    k: int = 5


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/ask")
def ask(request: AskRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question must not be empty")

    try:
        return run_pipeline(question, k=request.k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
