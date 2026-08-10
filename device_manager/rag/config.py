import os
from pathlib import Path
from config import BASE_DIR, UPLOAD_DIR

# RAG Directories
RAG_DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = RAG_DATA_DIR / "vector_store"
DOCUMENTS_DIR = RAG_DATA_DIR / "documents"

# Ensure directories exist
RAG_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Chunking & Embedding Parameters
CHUNK_SIZE = 600       # Target characters/tokens per chunk
CHUNK_OVERLAP = 120    # Overlap between chunks
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Retrieval Parameters
DEFAULT_TOP_K = 5
RAG_MIN_SCORE = 0.15   # Minimum cosine similarity score threshold

# File Limits & Security Exclusions
MAX_DOCUMENT_SIZE_MB = 10
SUPPORTED_EXTENSIONS = {".txt", ".md", ".py", ".json", ".csv"}
SENSITIVE_EXCLUSION_PATTERNS = [
    ".env", "*.pem", "*.key", "credentials*", "passwords*", "*id_rsa*", "*.db", "*.faiss"
]
