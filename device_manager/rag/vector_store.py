import os
from pathlib import Path
import numpy as np
import faiss
from typing import List, Tuple
from rag.config import VECTOR_STORE_DIR, EMBEDDING_DIM

INDEX_FILE = VECTOR_STORE_DIR / "index.faiss"

class PersistentVectorStore:
    """
    Persistent Local FAISS Vector Database using IndexFlatIP & IndexIDMap2.
    Vector positions map 1-to-1 to persistent integer IDs surviving server restarts.
    """
    def __init__(self, dim: int = EMBEDDING_DIM):
        self.dim = dim
        self.index_file = INDEX_FILE
        self.index = None
        self.load()

    def _create_new_index(self):
        flat_index = faiss.IndexFlatIP(self.dim)
        self.index = faiss.IndexIDMap2(flat_index)

    def load(self) -> bool:
        if self.index_file.exists():
            try:
                self.index = faiss.read_index(str(self.index_file))
                print(f"[FAISS VECTOR STORE]: Loaded persistent index with {self.index.ntotal} vectors.")
                return True
            except Exception as e:
                print(f"[FAISS VECTOR STORE WARNING]: Failed to load index file: {e}. Recreating...")
                self._create_new_index()
                return False
        else:
            self._create_new_index()
            return False

    def save(self) -> bool:
        if self.index is not None:
            try:
                faiss.write_index(self.index, str(self.index_file))
                return True
            except Exception as e:
                print(f"[FAISS VECTOR STORE ERROR]: Failed to save index: {e}")
                return False
        return False

    def add_vectors(self, vectors: np.ndarray, ids: List[int]) -> bool:
        if vectors.shape[0] == 0 or len(ids) == 0:
            return False
        
        if self.index is None:
            self._create_new_index()

        faiss_ids = np.array(ids, dtype=np.int64)
        self.index.add_with_ids(vectors, faiss_ids)
        self.save()
        return True

    def remove_ids(self, ids: List[int]) -> bool:
        if not ids or self.index is None or self.index.ntotal == 0:
            return False

        try:
            faiss_ids = np.array(ids, dtype=np.int64)
            self.index.remove_ids(faiss_ids)
            self.save()
            return True
        except Exception as e:
            print(f"[FAISS VECTOR STORE WARNING]: Error removing IDs: {e}")
            return False

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> Tuple[List[float], List[int]]:
        if self.index is None or self.index.ntotal == 0:
            return [], []

        actual_k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(query_vector, actual_k)
        
        scores = distances[0].tolist()
        ids = indices[0].tolist()
        
        # Filter out invalid FAISS unassigned index -1
        valid_scores = []
        valid_ids = []
        for s, i in zip(scores, ids):
            if i != -1:
                valid_scores.append(float(s))
                valid_ids.append(int(i))
                
        return valid_scores, valid_ids

    def clear(self) -> bool:
        self._create_new_index()
        if self.index_file.exists():
            try:
                os.remove(self.index_file)
            except Exception:
                pass
        return True

    @property
    def total_vectors(self) -> int:
        return self.index.ntotal if self.index is not None else 0

vector_store = PersistentVectorStore()
