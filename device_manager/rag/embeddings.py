import numpy as np
from typing import List
from rag.config import EMBEDDING_MODEL_NAME

class EmbeddingEngine:
    """
    Singleton local embedding engine using Sentence-Transformers (all-MiniLM-L6-v2).
    Generates normalized 384-dimensional vector embeddings for cosine similarity.
    """
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if EmbeddingEngine._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                EmbeddingEngine._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
                print(f"[RAG EMBEDDINGS]: Loaded local model '{EMBEDDING_MODEL_NAME}'.")
            except Exception as e:
                print(f"[RAG EMBEDDINGS ERROR]: Failed to load '{EMBEDDING_MODEL_NAME}': {e}")
                EmbeddingEngine._model = None

    def embed_documents(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        if not texts or EmbeddingEngine._model is None:
            return np.zeros((0, 384), dtype=np.float32)

        embeddings = EmbeddingEngine._model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True # Unit vectors for Cosine Similarity via Inner Product
        )
        return np.array(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        if not query or EmbeddingEngine._model is None:
            return np.zeros((1, 384), dtype=np.float32)

        embedding = EmbeddingEngine._model.encode(
            [query],
            show_progress_bar=False,
            normalize_embeddings=True
        )
        return np.array(embedding, dtype=np.float32)

embedding_engine = EmbeddingEngine()
