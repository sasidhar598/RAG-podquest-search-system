# podquest-harika
Problem Statement

Long podcast episodes contain valuable insights, but users can’t quickly locate where a topic is discussed. Manual scrubbing is slow and error-prone. We need a system that makes podcasts semantically searchable and returns timestamped evidence across episodes.

Long podcasts are hard to navigate. Users need to find where a topic was discussed, with evidence (timestamps). Manual scrubbing is slow and inaccurate.

Why Multi-Agent

The pipeline is naturally modular: ingesting audio, transcribing, chunking, embedding, indexing, retrieval, and quality checks are distinct expert roles. Specialized agents working in parallel improve speed, reliability, and maintainability. A supervisor coordinates them, retries failures, and enforces quality (e.g., “include timestamps” guardrails).
The pipeline (ingest → transcription → chunking → indexing → retrieval → QA) maps naturally to specialized agents. Multi-agent orchestration improves speed (parallel steps), quality (specialists), and reliability (supervisor & guardrails).

Application

Streamlit app to upload podcasts, transcribe to timestamped text, index as vectors, and semantically search topics across episodes. Results include episode + timestamped transcript.

Agents & Interaction

Supervisor → coordinates flow, retries failures

Ingestion → validates/normalizes audio

Transcription → Faster-Whisper → JSON segments

Segmentation/Indexing → chunk + embed (Sentence-Transformers), upsert to ChromaDB

Retrieval/Q&A → semantic search + extractive response

Evaluation/Guardrails → verify timestamps and citation to transcripts

Technologies used

Python, Streamlit, Faster-Whisper, Sentence-Transformers, ChromaDB, CrewAI (or LangGraph), pydub/ffmpeg, numpy/pandas

LLMs

Ideal: GPT-4o-mini / Claude 3.5 Sonnet / Gemini 1.5 Pro

Free: Gemini 1.5 Flash (free tier) or Llama 3.1 8B via Ollama
Choose based on cost, latency, and reliability; the LLM mainly formats/coordinates since retrieval is embedding-based.
