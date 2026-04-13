# podquest/config.py
# Central configuration for the PodQuest app.

from pathlib import Path
import os

# ---------- Paths ----------
# Project root = two levels up from this file: .../PODQUEST-HARIKA
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = DATA_DIR / "chroma"   # folder on disk for Chroma persistence
# Some parts of your app may expect plain strings:
CHROMA_DIR_STR = str(CHROMA_DIR)

# ---------- ChromaDB ----------
# Local persistent client folder + collection name
CHROMA_COLLECTION = "podquest"

# If you ever switch to HTTP Chroma server, set these (not used by default):
CHROMA_HOST = os.getenv("CHROMA_HOST", "http://localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# ---------- Audio / Whisper ----------
# Options for faster-whisper compute_type: "int8", "int8_float16", "float16", "float32"
DEFAULT_WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
DEFAULT_COMPUTE_TYPE  = os.getenv("WHISPER_COMPUTE_TYPE", "int8")  # good CPU default

# Chunking used when slicing long audio for transcription
CHUNK_SEC          = int(os.getenv("CHUNK_SEC", "30"))
CHUNK_OVERLAP_SEC  = int(os.getenv("CHUNK_OVERLAP_SEC", "5"))

# ---------- Embeddings ----------
# Choose backend: "sbert" (local Sentence-Transformers) or "openai"
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "sbert")

# Local SBERT model (small, fast, good quality)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# OpenAI settings (only used if EMBEDDING_BACKEND == "openai")
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# ---------- Retrieval ----------
# How many results to fetch per query
TOP_K = int(os.getenv("TOP_K", "5"))

# If you filter by *similarity score*, keep results >= SCORE_THRESHOLD.
# (If your code uses distance instead, set/use MAX_DISTANCE there.)
SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.2"))

# Toggle whether to apply score thresholding in retrieval
USE_SCORE_THRESHOLD = os.getenv("USE_SCORE_THRESHOLD", "true").lower() in {"1", "true", "yes"}

# ---------- Backward-compat aliases ----------
# Some earlier snippets/packages may import these names.
try:
    EMBEDDING_MODEL_NAME  # type: ignore
except NameError:
    EMBEDDING_MODEL_NAME = EMBEDDING_MODEL

try:
    N_RESULTS  # type: ignore
except NameError:
    N_RESULTS = TOP_K

try:
    MIN_SCORE  # type: ignore
except NameError:
    MIN_SCORE = SCORE_THRESHOLD
