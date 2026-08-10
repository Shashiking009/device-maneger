import os
from pathlib import Path

# Centralized System & Network Configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8088"))
SERVER_URL = f"http://{HOST}:{PORT}"

# Ollama SLM Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

# Base Paths & Portable Directories
BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR.parent
UPLOAD_DIR = BASE_DIR / "uploaded_docs"
DATABASE_PATH = BASE_DIR / "device_manager.db"
VECTOR_STORE_PATH = BASE_DIR / "vector_store"

# Ensure runtime folders exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
