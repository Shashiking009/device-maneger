import os
import time
from pathlib import Path
from typing import Dict, Any, List
from rag.loader import loader
from rag.cleaner import cleaner
from rag.chunker import chunker
from rag.embeddings import embedding_engine
from rag.vector_store import vector_store
from rag.metadata_store import metadata_store

class IncrementalIndexer:
    """
    Incremental Document Indexer using SHA-256 Content Hashing.
    Skips unchanged files, re-indexes modified files, indexes new files, and purges deleted files.
    """
    def index_file(self, filepath: str) -> Dict[str, Any]:
        start_t = time.time()
        doc = loader.load(filepath)
        if not doc:
            return {"status": "skipped", "reason": "Unreadable or unsupported file format", "filepath": filepath}

        doc_path = doc.path
        existing_info = metadata_store.get_doc_info(doc_path)

        # Check hash to skip unchanged file
        if existing_info and existing_info.get("document_hash") == doc.document_hash:
            return {"status": "skipped", "reason": "Unchanged (SHA-256 match)", "filepath": doc_path}

        # If modified, remove old vector IDs first
        if existing_info:
            old_ids = metadata_store.remove_document(doc_path)
            vector_store.remove_ids(old_ids)

        # Chunk document
        chunks = chunker.chunk_document(doc)
        if not chunks:
            return {"status": "skipped", "reason": "No text content after chunking", "filepath": doc_path}

        # Batch embed chunks
        texts = [c.text for c in chunks]
        embeddings = embedding_engine.embed_documents(texts)

        # Store metadata and get assigned FAISS integer IDs
        assigned_ids = metadata_store.add_chunks(chunks)

        # Add vectors to persistent FAISS index
        vector_store.add_vectors(embeddings, assigned_ids)

        elapsed_ms = round((time.time() - start_t) * 1000, 2)
        return {
            "status": "reindexed" if existing_info else "indexed",
            "filepath": doc_path,
            "filename": doc.filename,
            "chunks_count": len(chunks),
            "time_ms": elapsed_ms
        }

    def index_directory(self, dir_path: str) -> Dict[str, Any]:
        start_t = time.time()
        target_dir = Path(dir_path).resolve()
        
        if not target_dir.is_dir():
            return {"status": "error", "message": f"Directory not found: {dir_path}"}

        found_paths = set()
        indexed_count = 0
        skipped_count = 0
        reindexed_count = 0
        total_chunks = 0

        # 1. Scan directory recursively
        for root, _, files in os.walk(target_dir):
            for file in files:
                fpath = str(Path(root) / file)
                res = self.index_file(fpath)
                found_paths.add(fpath)
                
                status = res.get("status")
                if status == "indexed":
                    indexed_count += 1
                    total_chunks += res.get("chunks_count", 0)
                elif status == "reindexed":
                    reindexed_count += 1
                    total_chunks += res.get("chunks_count", 0)
                elif status == "skipped":
                    skipped_count += 1

        # 2. Detect deleted files previously in manifest
        deleted_count = 0
        tracked_paths = list(metadata_store.manifest.documents.keys())
        for tracked in tracked_paths:
            # If tracked file belonged to target_dir but no longer exists on disk
            if tracked.startswith(str(target_dir)) and not os.path.exists(tracked):
                old_ids = metadata_store.remove_document(tracked)
                vector_store.remove_ids(old_ids)
                deleted_count += 1

        elapsed_ms = round((time.time() - start_t) * 1000, 2)
        return {
            "status": "success",
            "directory": str(target_dir),
            "new_indexed": indexed_count,
            "reindexed": reindexed_count,
            "skipped": skipped_count,
            "deleted": deleted_count,
            "chunks_added": total_chunks,
            "total_chunks_in_db": vector_store.total_vectors,
            "time_ms": elapsed_ms
        }

    def remove_file(self, filepath: str) -> bool:
        path = str(Path(filepath).resolve())
        old_ids = metadata_store.remove_document(path)
        if old_ids:
            vector_store.remove_ids(old_ids)
            return True
        return False

    def clear_all(self):
        metadata_store.clear()
        vector_store.clear()

indexer = IncrementalIndexer()
