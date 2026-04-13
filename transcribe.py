# podquest/transcribe.py
import os, json
from typing import Dict, List
from faster_whisper import WhisperModel
from .utils import ensure_dir, clean_text

def _join_segments(segments: List[Dict]) -> str:
    return " ".join(seg["text"] for seg in segments).strip()

def read_transcript(json_path: str) -> Dict:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["text"] = _join_segments(data.get("segments", []))
    return data

def transcribe_file(audio_path: str, out_dir: str, model_size="base", compute_type="int8") -> Dict:
    """
    Transcribe an audio file and write a JSON next to `out_dir`.
    Returns: {"json_path": <path>, "segments": [...], "text": "..."}
    """
    ensure_dir(out_dir)

    model = WhisperModel(model_size, compute_type=compute_type)
    segments, _ = model.transcribe(audio_path)

    # convert generator → list of dicts
    segs = []
    for s in segments:
        segs.append({
            "start": round(float(s.start), 2),
            "end": round(float(s.end), 2),
            "text": clean_text(s.text),
        })

    base = os.path.splitext(os.path.basename(audio_path))[0]
    json_path = os.path.join(out_dir, f"{base}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"segments": segs}, f, ensure_ascii=False, indent=2)

    return {"json_path": json_path, "segments": segs, "text": _join_segments(segs)}
