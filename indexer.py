import os, json, uuid
from typing import Dict, Any, List, Tuple
import chromadb
from sentence_transformers import SentenceTransformer
from .utils import ensure_dir
from .config import EMBEDDING_MODEL, CHROMA_COLLECTION, CHROMA_DIR, CHUNK_SEC, CHUNK_OVERLAP_SEC

def load_json(p: str) -> Dict[str, Any]:
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_timestamped(segments: List[Dict[str, Any]], win: int, overlap: int) -> List[Dict[str, Any]]:
    if not segments: return []
    chunks, cur = [], segments[0]["start"]
    total_end = segments[-1]["end"]
    while cur < total_end:
        end = cur + win
        texts = [s["text"] for s in segments if not (s["end"] <= cur or s["start"] >= end)]
        txt = " ".join(texts).strip()
        if txt:
            chunks.append({"start": cur, "end": min(end, total_end), "text": txt})
        cur = cur + (win - overlap)
    return chunks

def build_index(transcript_dir: str) -> Tuple[int, str]:
    ensure_dir(CHROMA_DIR)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        coll = client.get_collection(CHROMA_COLLECTION)
    except Exception:
        coll = client.create_collection(CHROMA_COLLECTION)

    embedder = SentenceTransformer(EMBEDDING_MODEL)
    added = 0

    for name in os.listdir(transcript_dir):
        if not name.endswith(".json"): continue
        path = os.path.join(transcript_dir, name)
        doc = load_json(path)
        episode = os.path.splitext(name)[0]
        chunks = chunk_timestamped(doc.get("segments", []), CHUNK_SEC, CHUNK_OVERLAP_SEC)
        if not chunks: continue

        ids, docs, metas = [], [], []
        for i, ch in enumerate(chunks):
            ids.append(f"{episode}-{i}-{uuid.uuid4().hex[:6]}")
            docs.append(ch["text"])
            metas.append({
                "episode": episode,
                "audio_file": doc.get("audio_file"),
                "start": float(ch["start"]),
                "end": float(ch["end"])
            })

        embs = embedder.encode(docs, convert_to_numpy=True, normalize_embeddings=True)
        coll.add(ids=ids, embeddings=embs, documents=docs, metadatas=metas)
        added += len(ids)

    return added, CHROMA_DIR
