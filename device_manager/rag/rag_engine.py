import time
from typing import Dict, Any, List, Optional
from rag.config import DOCUMENTS_DIR, DEFAULT_TOP_K, RAG_MIN_SCORE, EMBEDDING_MODEL_NAME
from rag.models import RAGQueryResponse, RAGStatusResponse, SearchResult
from rag.retriever import retriever
from rag.indexer import indexer
from rag.vector_store import vector_store
from rag.metadata_store import metadata_store
from rag.prompts import build_rag_prompt
from ai.qwen_engine import qwen_engine

class RAGEngine:
    """
    Unified High-Level Local RAG Engine Service API.
    Handles semantic search, grounded Qwen3 answer generation, source attribution, and incremental indexing.
    """
    def query(self, question: str, top_k: int = DEFAULT_TOP_K, min_score: float = RAG_MIN_SCORE) -> RAGQueryResponse:
        start_t = time.time()
        
        # 1. Retrieve relevant chunks using FAISS
        search_results = retriever.search(question, top_k=top_k, min_score=min_score)

        # Hallucination Protection: If no chunk meets minimum similarity score, return grounded refusal
        if not search_results:
            elapsed_ms = round((time.time() - start_t) * 1000, 2)
            return RAGQueryResponse(
                success=True,
                answer="I couldn't find relevant information in your indexed documents.",
                sources=[],
                search_results=[],
                tps=0.0,
                query_time_ms=elapsed_ms
            )

        # 2. Build RAG prompt with deduplicated source citations
        prompt, sources = build_rag_prompt(question, search_results)

        # 3. Generate grounded answer via Qwen3 SLM
        answer, tps = qwen_engine.generate_ai_response(prompt, temperature=0.2)

        # Append formatted source citations footer if not present
        if sources and "Sources:" not in answer:
            sources_footer = "\n\nSources:\n" + "\n".join([f"- {src}" for src in sources])
            answer = answer + sources_footer

        elapsed_ms = round((time.time() - start_t) * 1000, 2)
        return RAGQueryResponse(
            success=True,
            answer=answer,
            sources=sources,
            search_results=search_results,
            tps=tps,
            query_time_ms=elapsed_ms
        )

    def index(self, path: str) -> Dict[str, Any]:
        if os.path.isdir(path):
            return indexer.index_directory(path)
        else:
            return indexer.index_file(path)

    def reindex(self, path: str) -> Dict[str, Any]:
        return self.index(path)

    def remove(self, path: str) -> bool:
        return indexer.remove_file(path)

    def clear(self):
        indexer.clear_all()

    def status(self) -> RAGStatusResponse:
        docs_count = len(metadata_store.manifest.documents)
        chunks_count = vector_store.total_vectors
        return RAGStatusResponse(
            ready=True,
            status="READY" if chunks_count > 0 else "IDLE",
            documents_count=docs_count,
            chunks_count=chunks_count,
            embedding_model=EMBEDDING_MODEL_NAME,
            vector_store="FAISS (IndexFlatIP + IndexIDMap2)",
            persistent=True
        )

import os
rag_service = RAGEngine()
