import os
import re
import math
import json
from typing import List, Dict, Any, Tuple
from config import UPLOAD_DIR

UPLOAD_DIR = str(UPLOAD_DIR)

class RAGEngine:
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def _clean_text(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9_]{2,}\b', text.lower())
        return words

    def chunk_document(self, filename: str, filepath: str, text: str, chunk_size: int = 400, overlap: int = 80) -> List[Dict[str, Any]]:
        cleaned = self._clean_text(text)
        words = cleaned.split(" ")
        
        doc_chunks = []
        step = chunk_size - overlap
        if step <= 0:
            step = chunk_size
            
        for i in range(0, len(words), step):
            chunk_words = words[i:i + chunk_size]
            if len(chunk_words) < 15 and i > 0:
                continue
            chunk_text = " ".join(chunk_words)
            chunk_id = f"{filename}_chunk_{len(doc_chunks)}"
            doc_chunks.append({
                "id": chunk_id,
                "filename": filename,
                "filepath": filepath,
                "text": chunk_text,
                "tokens": self._tokenize(chunk_text)
            })
            
        self.chunks.extend(doc_chunks)
        self._rebuild_tfidf()
        return doc_chunks

    def _rebuild_tfidf(self):
        N = len(self.chunks)
        if N == 0:
            return

        df: Dict[str, int] = {}
        for chunk in self.chunks:
            unique_terms = set(chunk["tokens"])
            for term in unique_terms:
                df[term] = df.get(term, 0) + 1

        self.idf = {term: math.log((N + 1) / (count + 1)) + 1 for term, count in df.items()}

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.chunks:
            return []

        scores: List[Tuple[float, Dict[str, Any]]] = []

        for chunk in self.chunks:
            chunk_tokens = chunk["tokens"]
            if not chunk_tokens:
                continue
            
            tf: Dict[str, int] = {}
            for t in chunk_tokens:
                tf[t] = tf.get(t, 0) + 1

            score = 0.0
            for qt in query_tokens:
                if qt in tf:
                    score += (tf[qt] / len(chunk_tokens)) * self.idf.get(qt, 1.0)

            if score > 0:
                scores.append((score, chunk))

        scores.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, chunk in scores[:top_k]:
            results.append({
                "score": round(score, 4),
                "filename": chunk["filename"],
                "chunk_id": chunk["id"],
                "snippet": chunk["text"][:300] + "..." if len(chunk["text"]) > 300 else chunk["text"]
            })
        return results

    def remove_document_chunks(self, filename: str):
        self.chunks = [c for c in self.chunks if c["filename"] != filename]
        self._rebuild_tfidf()

rag_engine = RAGEngine()

if __name__ == "__main__":
    test_text = "Device Manager uses Qwen3 Small Language Model for fast offline inference. It runs locally via Ollama."
    rag_engine.chunk_document("test.txt", "/tmp/test.txt", test_text)
    res = rag_engine.search("What model does Device Manager use?")
    print("Search result:", res)
