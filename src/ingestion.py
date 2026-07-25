"""Load, chunk, embed, and index documents from docs/ into a local FAISS index."""

import json
import os

import faiss
import numpy as np

from src.embeddings import EMBEDDING_MODEL_NAME, get_embedding_model

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "index")
INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(INDEX_DIR, "chunks.json")

CHUNK_SIZE_WORDS = 500
CHUNK_OVERLAP_WORDS = 50


def load_documents(docs_dir=DOCS_DIR):
    """Read every .txt file in docs_dir, returning [{"source": filename, "text": ...}]."""
    documents = []
    for filename in sorted(os.listdir(docs_dir)):
        if not filename.lower().endswith(".txt"):
            continue
        path = os.path.join(docs_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        documents.append({"source": filename, "text": text})
    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE_WORDS, overlap=CHUNK_OVERLAP_WORDS):
    """Split text into overlapping word-count chunks (word count approximates token count)."""
    words = text.split()
    if not words:
        return []
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break
    return chunks


def build_chunks(documents):
    """Chunk every document, returning a flat list of {"source", "chunk_id", "text"}."""
    chunks = []
    for doc in documents:
        for i, chunk in enumerate(chunk_text(doc["text"])):
            chunks.append({"source": doc["source"], "chunk_id": i, "text": chunk})
    return chunks


def build_index(docs_dir=DOCS_DIR, index_dir=INDEX_DIR):
    """Full ingestion pipeline: load -> chunk -> embed -> build FAISS index -> persist to disk."""
    os.makedirs(index_dir, exist_ok=True)

    documents = load_documents(docs_dir)
    if not documents:
        raise ValueError(f"No .txt documents found in {docs_dir}")

    chunks = build_chunks(documents)
    if not chunks:
        raise ValueError("Documents were loaded but produced no chunks")

    model = get_embedding_model()
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity via normalized inner product
    index.add(embeddings)

    faiss.write_index(index, os.path.join(index_dir, "faiss.index"))
    with open(os.path.join(index_dir, "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return index, chunks


def index_exists(index_dir=INDEX_DIR):
    return os.path.exists(os.path.join(index_dir, "faiss.index")) and os.path.exists(
        os.path.join(index_dir, "chunks.json")
    )


if __name__ == "__main__":
    index, chunks = build_index()
    print(f"Indexed {len(chunks)} chunks from {DOCS_DIR} into {INDEX_DIR}")
