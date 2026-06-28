import json
import re
from pathlib import Path

from infrastructure.data_access import PROJECT_ROOT

KB_PATH = PROJECT_ROOT / "data" / "knowledge_base"
VECTOR_STORE_PATH = Path(__file__).parent / "faiss_index"
MANIFEST_PATH = VECTOR_STORE_PATH / "documents.json"


def build_vector_store() -> int:
    docs = _load_documents()
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(docs, indent=2), encoding="utf-8")

    if not _should_build_faiss_embeddings():
        return len(docs)

    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        vectors = model.encode([doc["text"] for doc in docs], normalize_embeddings=True)
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(np.asarray(vectors, dtype="float32"))
        faiss.write_index(index, str(VECTOR_STORE_PATH / "faiss.index"))
    except Exception:
        pass

    return len(docs)


def search_knowledge_base(query: str, k: int = 3) -> list[dict]:
    docs = _stored_or_loaded_documents()
    if not docs:
        return []

    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer

        index_path = VECTOR_STORE_PATH / "faiss.index"
        if index_path.exists() and _should_build_faiss_embeddings():
            model = SentenceTransformer("all-MiniLM-L6-v2")
            vector = model.encode([query], normalize_embeddings=True)
            index = faiss.read_index(str(index_path))
            scores, indices = index.search(np.asarray(vector, dtype="float32"), k)
            return [
                {**docs[i], "score": float(scores[0][rank])}
                for rank, i in enumerate(indices[0])
                if 0 <= i < len(docs)
            ]
    except Exception:
        pass

    return _lexical_search(query, docs, k)


def _load_documents() -> list[dict]:
    docs = []
    for path in KB_PATH.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        chunks = _chunk(text)
        for idx, chunk in enumerate(chunks):
            docs.append(
                {
                    "source": str(path.relative_to(KB_PATH)).replace("\\", "/"),
                    "chunk": idx,
                    "text": chunk,
                }
            )
    return docs


def _stored_or_loaded_documents() -> list[dict]:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return _load_documents()


def _chunk(text: str, size: int = 900) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) > size and current:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}".strip()
    if current:
        chunks.append(current)
    return chunks


def _lexical_search(query: str, docs: list[dict], k: int) -> list[dict]:
    terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = []
    for doc in docs:
        text_terms = set(re.findall(r"[a-z0-9]+", doc["text"].lower()))
        score = len(terms & text_terms)
        if score:
            scored.append({**doc, "score": float(score)})
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored[:k] if scored else docs[:k]


def _should_build_faiss_embeddings() -> bool:
    import os

    return os.getenv("BUILD_FAISS_EMBEDDINGS") == "1"
