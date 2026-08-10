import time
from typing import List
from rag.config import DEFAULT_TOP_K, RAG_MIN_SCORE
from rag.models import SearchResult
from rag.embeddings import embedding_engine
from rag.vector_store import vector_store
from rag.metadata_store import metadata_store

class SemanticRetriever:
    """
    Semantic Document Retriever using FAISS Cosine Similarity.
    Filters out low-confidence results below RAG_MIN_SCORE threshold to prevent hallucination.
    """
    def search(self, query: str, top_k: int = DEFAULT_TOP_K, min_score: float = RAG_MIN_SCORE) -> List[SearchResult]:
        if not query.strip() or vector_store.total_vectors == 0:
            return []

        # 1. Embed query vector
        query_vec = embedding_engine.embed_query(query)

        # 2. Search FAISS index
        scores, faiss_ids = vector_store.search(query_vec, top_k=top_k)

        results = []
        for score, fid in zip(scores, faiss_ids):
            if score < min_score:
                continue

            chunk_info = metadata_store.get_chunk(fid)
            if not chunk_info:
                continue

            text_content = chunk_info.get("text", "")
            meta_dict = chunk_info.get("metadata", {})

            results.append(SearchResult(
                content=text_content,
                source_path=meta_dict.get("source_path", ""),
                filename=meta_dict.get("filename", "Unknown"),
                score=round(score, 4),
                chunk_id=meta_dict.get("chunk_id", str(fid)),
                extension=meta_dict.get("extension", "")
            ))

        return results

retriever = SemanticRetriever()
