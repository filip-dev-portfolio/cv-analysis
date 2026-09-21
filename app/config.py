import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CV_DIR = DATA_DIR / "cvs"
JOB_DIR = DATA_DIR / "jobs"
RESULT_DIR = DATA_DIR / "results"

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://host.docker.internal:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:8b",
)

MAX_CV_SIZE_MB = int(os.getenv("MAX_CV_SIZE_MB", "10"))


def ensure_directories() -> None:
    CV_DIR.mkdir(parents=True, exist_ok=True)
    JOB_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
