# app.py (only the relevant bits)
import os, time, json
import streamlit as st

from podquest.transcribe import transcribe_file, read_transcript
from podquest.config import DEFAULT_WHISPER_MODEL, DEFAULT_COMPUTE_TYPE
from pathlib import Path

TRANSCRIPTS_DIR = Path("transcripts")
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

st.title("Ingest & Transcribe")

uploaded_files = st.file_uploader(
    "Upload episodes", type=["mp3", "wav"], accept_multiple_files=True
)

saved_paths = []
if uploaded_files:
    for uf in uploaded_files:
        save_path = Path("data") / uf.name
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uf.getbuffer())
        st.success(f"Saved: {save_path}")
        saved_paths.append(str(save_path))

# --- Transcribe everything that was just uploaded ---
if st.button("Transcribe all") and saved_paths:
    for p in saved_paths:
        with st.spinner(f"Transcribing {os.path.basename(p)} ..."):
            result = transcribe_file(
                audio_path=p,
                out_dir=str(TRANSCRIPTS_DIR),
                model_size=DEFAULT_WHISPER_MODEL,
                compute_type=DEFAULT_COMPUTE_TYPE,
            )
        st.success(f"Saved transcript: {result['json_path']}")

        # Show the transcript text right away
        st.subheader(f"Transcript: {os.path.basename(result['json_path'])}")
        st.text_area(
            "Full transcript",
            value=result["text"],
            height=220,
            key=f"ta_{result['json_path']}",
        )

        # Optional: show segments table
        if st.checkbox("Show segments with timestamps", key=f"cb_{result['json_path']}"):
            import pandas as pd
            st.dataframe(pd.DataFrame(result["segments"]))

        # Download buttons
        st.download_button(
            label="Download .txt",
            data=result["text"],
            file_name=os.path.basename(result["json_path"]).replace(".json", ".txt"),
            mime="text/plain",
            key=f"dl_txt_{result['json_path']}",
        )
        st.download_button(
            label="Download .json",
            data=json.dumps({"segments": result["segments"]}, ensure_ascii=False, indent=2),
            file_name=os.path.basename(result["json_path"]),
            mime="application/json",
            key=f"dl_json_{result['json_path']}",
        )

st.markdown("---")

# --- Viewer: open any existing transcript from /transcripts ---
existing = sorted([p for p in TRANSCRIPTS_DIR.glob("*.json")])
if existing:
    pick = st.selectbox(
        "Open an existing transcript",
        options=[str(p) for p in existing],
        format_func=lambda p: os.path.basename(p),
    )
    if pick:
        data = read_transcript(pick)
        st.subheader(f"Transcript: {os.path.basename(pick)}")
        st.text_area("Full transcript", value=data["text"], height=220, key=f"view_{pick}")

        if st.checkbox("Show segments with timestamps", key=f"seg_view_{pick}"):
            import pandas as pd
            st.dataframe(pd.DataFrame(data["segments"]))
else:
    st.info("No saved transcripts yet. Upload audio and click **Transcribe all**.")
