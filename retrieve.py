from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DIR, TOP_K, SCORE_THRESHOLD
from .utils import sec_to_hhmmss

def _coll():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(CHROMA_COLLECTION)

def _embed(q: str):
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model.encode([q], convert_to_numpy=True, normalize_embeddings=True)[0]

def search(query: str, top_k: int = TOP_K, score_thr: float = SCORE_THRESHOLD) -> List[Dict[str, Any]]:
    coll = _coll()
    vec = _embed(query)
    res = coll.query(query_embeddings=[vec], n_results=top_k*2)

    out = []
    for i in range(len(res["ids"][0])):
        d = float(res["distances"][0][i])
        if d <= score_thr:
            meta = res["metadatas"][0][i]
            out.append({
                "score": d,
                "text": res["documents"][0][i],
                "episode": meta.get("episode"),
                "audio_file": meta.get("audio_file"),
                "start": meta.get("start"),
                "end": meta.get("end"),
                "start_hms": sec_to_hhmmss(meta.get("start", 0)),
                "end_hms": sec_to_hhmmss(meta.get("end", 0))
            })
    out.sort(key=lambda x: x["score"])
    return out[:top_k]

def synthesize_answer(query: str, hits: List[Dict[str, Any]]) -> str:
    if not hits:
        return "No strong matches found. Try rephrasing or lower the strictness."
    lines = []
    for h in hits:
        lines.append(f"[{h['episode']}] {h['start_hms']}–{h['end_hms']}: {h['text']}")
    return "Relevant mentions across episodes:\n\n" + "\n".join("- " + l for l in lines)
