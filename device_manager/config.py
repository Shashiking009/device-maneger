import os
from pathlib import Path

# Centralized System & Network Configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8088"))
SERVER_URL = f"http://{HOST}:{PORT}"
VERSION = "1.0.0"

# Ollama SLM Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

# Base Paths & Portable Directories
BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploaded_docs"
DATABASE_PATH = DATA_DIR / "device_manager.db"
BACKUP_DIR = DATA_DIR / "backups"
VECTOR_STORE_PATH = DATA_DIR / "vector_store"

# Ensure runtime folders exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
