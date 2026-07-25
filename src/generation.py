"""Call an LLM via OpenRouter with retrieved context to generate an answer."""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-sonnet-4.6"

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the provided context. "
    "If the context does not contain enough information to answer, say so explicitly instead "
    "of guessing. Do not use outside knowledge beyond the provided context."
)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
    return _client


def build_context_block(chunks):
    """Render retrieved chunks into a single context string with source labels."""
    parts = []
    for c in chunks:
        parts.append(f"[Source: {c['source']} #{c['chunk_id']}]\n{c['text']}")
    return "\n\n".join(parts)


def generate_answer(question, chunks, model=DEFAULT_MODEL, temperature=0.0, max_tokens=512):
    """Generate an answer to `question` grounded in the given retrieved `chunks`."""
    client = _get_client()
    context = build_context_block(chunks)

    user_prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above."
    )

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    from src.retrieval import retrieve

    question = "What is RAG and why does it help with hallucination?"
    top_chunks = retrieve(question, k=4)
    answer = generate_answer(question, top_chunks)
    print(answer)
