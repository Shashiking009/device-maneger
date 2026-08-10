import sys
import os
import time
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.loader import loader
from rag.cleaner import cleaner
from rag.chunker import chunker
from rag.embeddings import embedding_engine
from rag.vector_store import vector_store
from rag.metadata_store import metadata_store
from rag.indexer import indexer
from rag.retriever import retriever
from rag.rag_engine import rag_service
from core.orchestrator import orchestrator
from core.intent_models import IntentType

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "rag")

def test_loader_and_formats():
    print("\n--- TEST 1: DOCUMENT LOADER & FORMAT SUPPORT ---")
    formats = ["project.md", "python.py", "notes.txt", "config.json", "data.csv"]
    for fmt in formats:
        fpath = os.path.join(FIXTURES_DIR, fmt)
        doc = loader.load(fpath)
        assert doc is not None, f"Failed to load format {fmt}"
        assert len(doc.text) > 0, f"Empty text for format {fmt}"
        assert len(doc.document_hash) == 64, f"Invalid SHA-256 hash length for {fmt}"
        print(f"  [PASS] Format '{fmt}' loaded cleanly ({doc.size_bytes} bytes | hash: {doc.document_hash[:8]}...)")

def test_hashing_consistency():
    print("\n--- TEST 2: SHA-256 HASHING CONSISTENCY ---")
    fpath = os.path.join(FIXTURES_DIR, "project.md")
    doc1 = loader.load(fpath)
    doc2 = loader.load(fpath)
    assert doc1.document_hash == doc2.document_hash, "Hashing same file produced different SHA-256 hashes"
    print(f"  [PASS] Hash consistency verified (SHA-256: {doc1.document_hash[:12]})")

def test_chunking_and_metadata():
    print("\n--- TEST 3: INTELLIGENT CHUNKING & METADATA ---")
    fpath = os.path.join(FIXTURES_DIR, "project.md")
    doc = loader.load(fpath)
    chunks = chunker.chunk_document(doc)
    assert len(chunks) > 0, "No chunks generated"
    for c in chunks:
        assert c.metadata.document_hash == doc.document_hash
        assert c.metadata.filename == doc.filename
        assert len(c.metadata.content_hash) == 64
    print(f"  [PASS] Chunked '{doc.filename}' into {len(chunks)} chunks with complete metadata")

def test_embeddings():
    print("\n--- TEST 4: LOCAL EMBEDDING ENGINE ---")
    texts = ["Spidy AI local assistant", "Python machine learning testing"]
    vecs = embedding_engine.embed_documents(texts)
    assert vecs.shape == (2, 384), f"Expected shape (2, 384), got {vecs.shape}"
    # Verify unit L2 normalization for Cosine Similarity
    norm = float(np.linalg.norm(vecs[0]))
    assert abs(norm - 1.0) < 1e-3, f"Embeddings not unit normalized: {norm}"
    print(f"  [PASS] Embedding engine generated normalized {vecs.shape[1]}-dim vectors")

import numpy as np

def test_incremental_indexing():
    print("\n--- TEST 5: INCREMENTAL INDEXING (SKIP / NEW / MODIFIED / DELETE) ---")
    rag_service.clear()
    
    # 1. New Indexing
    res1 = rag_service.index(FIXTURES_DIR)
    assert res1.get("new_indexed") >= 5
    print(f"  [PASS] New indexing: {res1.get('new_indexed')} files indexed ({res1.get('chunks_added')} chunks)")

    # 2. Skip Unchanged
    res2 = rag_service.index(FIXTURES_DIR)
    assert res2.get("skipped") >= 5
    assert res2.get("new_indexed") == 0
    assert res2.get("reindexed") == 0
    print(f"  [PASS] Unchanged files cleanly skipped (0 re-embed overhead)")

    # 3. Modified File
    mod_path = os.path.join(FIXTURES_DIR, "temp_mod.txt")
    with open(mod_path, "w", encoding="utf-8") as f:
        f.write("Initial content for modification test.")
    res_mod1 = indexer.index_file(mod_path)
    assert res_mod1.get("status") == "indexed"

    with open(mod_path, "w", encoding="utf-8") as f:
        f.write("Updated content after modification for modification test.")
    res_mod2 = indexer.index_file(mod_path)
    assert res_mod2.get("status") == "reindexed"
    print(f"  [PASS] Modified file correctly detected and reindexed")

    # 4. Deleted File
    os.remove(mod_path)
    res_del = rag_service.index(FIXTURES_DIR)
    assert res_del.get("deleted") >= 1
    print(f"  [PASS] Deleted file detected and removed from index")

def test_retrieval_and_hallucination_protection():
    print("\n--- TEST 6: RETRIEVAL & HALLUCINATION PROTECTION ---")
    # Relevant Query
    res_rel = rag_service.query("What model does my project use?")
    assert res_rel.success is True
    assert len(res_rel.sources) > 0, "No sources retrieved for relevant query"
    print(f"  [PASS] Grounded retrieval succeeded with sources: {res_rel.sources}")

    # Irrelevant / Hallucination Query
    res_irrel = rag_service.query("What is quantum teleportation spacetime topology dynamics?")
    assert "couldn't find" in res_irrel.answer.lower()
    assert len(res_irrel.sources) == 0
    print(f"  [PASS] Grounded refusal triggered for unindexed question: '{res_irrel.answer}'")

def test_persistence_across_restarts():
    print("\n--- TEST 7: VECTOR DB & METADATA DISK PERSISTENCE ---")
    before_count = vector_store.total_vectors
    assert before_count > 0

    # Simulate restart by reloading vector_store and metadata_store from disk
    vector_store.load()
    metadata_store.load()

    after_count = vector_store.total_vectors
    assert after_count == before_count, f"Persistence mismatch: {after_count} vs {before_count}"
    
    # Query again after reload
    res = rag_service.query("What hardware requirements are needed?")
    assert res.success is True
    assert "notes.txt" in res.sources
    print(f"  [PASS] Persistent index survived reload ({after_count} vectors intact)")

def test_orchestrator_rag_integration():
    print("\n--- TEST 8: SPIDY ORCHESTRATOR RAG_QUERY INTEGRATION ---")
    resp = orchestrator.process_command("What does my project plan say about Qwen3?")
    assert resp.intent == IntentType.RAG_QUERY
    assert resp.success is True
    assert len(resp.sources) > 0
    print(f"  [PASS] Orchestrator routed RAG_QUERY -> Grounded Answer with sources: {[s['filename'] for s in resp.sources]}")

if __name__ == "__main__":
    print("======================================================")
    print("        SPIDY AI PHASE 3 RAG TEST SUITE              ")
    print("======================================================")
    test_loader_and_formats()
    test_hashing_consistency()
    test_chunking_and_metadata()
    test_embeddings()
    test_incremental_indexing()
    test_retrieval_and_hallucination_protection()
    test_persistence_across_restarts()
    test_orchestrator_rag_integration()
    print("\nALL PHASE 3 RAG TESTS PASSED SUCCESSFULLY!")
