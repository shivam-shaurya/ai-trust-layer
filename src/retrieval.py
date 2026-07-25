"""Query the FAISS index and return the top-k most relevant chunks with similarity scores."""

import json
import os

import faiss

from src.embeddings import get_embedding_model
from src.ingestion import CHUNKS_PATH, INDEX_PATH, build_index, index_exists

_index = None
_chunks = None


def _load_model():
    return get_embedding_model()


def _load_index():
    global _index, _chunks
    if _index is None or _chunks is None:
        if not index_exists():
            build_index()
        _index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            _chunks = json.load(f)
    return _index, _chunks


def retrieve(query, k=5):
    """Embed the query and return the top-k chunks as a list of
    {"source", "chunk_id", "text", "score"} sorted by descending similarity score.
    """
    model = _load_model()
    index, chunks = _load_index()

    query_embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    query_embedding = query_embedding.astype("float32")

    k = min(k, len(chunks))
    if k == 0:
        return []

    scores, indices = index.search(query_embedding, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = chunks[idx]
        results.append(
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "score": float(score),
            }
        )
    return results


def score_retrieval_quality(chunks, k_requested):
    """Score the quality of retrieved evidence for a query.

    Combines average similarity, top-1 similarity, source diversity (1 - average pairwise
    similarity between retrieved chunks), and coverage (chunks returned / chunks requested)
    into a single 0-1 quality score.

    Returns {"score", "avg_similarity", "top_similarity", "diversity", "coverage",
    "distinct_sources"}.
    """
    if not chunks:
        return {
            "score": 0.0,
            "avg_similarity": 0.0,
            "top_similarity": 0.0,
            "diversity": 0.0,
            "coverage": 0.0,
            "distinct_sources": 0,
        }

    scores = [c["score"] for c in chunks]
    avg_similarity = sum(scores) / len(scores)
    top_similarity = max(scores)
    distinct_sources = len(set(c["source"] for c in chunks))
    coverage = len(chunks) / k_requested if k_requested else 1.0

    model = _load_model()
    embeddings = model.encode(
        [c["text"] for c in chunks], convert_to_numpy=True, normalize_embeddings=True
    )
    if len(embeddings) > 1:
        sim_matrix = embeddings @ embeddings.T
        n = len(embeddings)
        pairwise = [sim_matrix[i][j] for i in range(n) for j in range(n) if i != j]
        diversity = 1.0 - (sum(pairwise) / len(pairwise))
    else:
        diversity = 0.0

    # avg_similarity/diversity/coverage are each already ~[0,1]; clamp for safety since
    # cosine similarity can dip slightly negative for unrelated text.
    quality_score = 0.5 * max(0.0, avg_similarity) + 0.3 * max(0.0, diversity) + 0.2 * min(
        1.0, coverage
    )

    return {
        "score": round(max(0.0, min(1.0, quality_score)), 3),
        "avg_similarity": round(avg_similarity, 3),
        "top_similarity": round(top_similarity, 3),
        "diversity": round(diversity, 3),
        "coverage": round(coverage, 3),
        "distinct_sources": distinct_sources,
    }


if __name__ == "__main__":
    chunks = retrieve("What is RAG?", k=3)
    for r in chunks:
        print(f"[{r['score']:.3f}] {r['source']}#{r['chunk_id']}: {r['text'][:80]}...")
    print("Retrieval quality:", score_retrieval_quality(chunks, k_requested=3))
