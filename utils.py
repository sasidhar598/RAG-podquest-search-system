import os, re, time

def ensure_dir(path):
    """Create the directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)
def clean_text(text):
    """Remove unwanted spaces and special characters."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def sec_to_hhmmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def timeit(fn):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        out = fn(*args, **kwargs)
        return out, time.time() - t0
    return wrapper

