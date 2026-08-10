import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from rag.config import VECTOR_STORE_DIR
from rag.models import Chunk, ChunkMetadata, IndexingManifest

METADATA_FILE = VECTOR_STORE_DIR / "metadata.json"
MANIFEST_FILE = VECTOR_STORE_DIR / "manifest.json"

class MetadataStore:
    """
    Synchronized metadata and incremental indexing manifest store.
    Survives server/computer restarts and guarantees FAISS vector position consistency.
    """
    def __init__(self):
        self.metadata_file = METADATA_FILE
        self.manifest_file = MANIFEST_FILE
        self.metadata: Dict[int, Dict[str, Any]] = {} # faiss_id -> chunk dict
        self.next_faiss_id = 0
        self.manifest = IndexingManifest()
        self.load()

    def load(self):
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.metadata = {int(k): v for k, v in data.get("chunks", {}).items()}
                    self.next_faiss_id = data.get("next_faiss_id", len(self.metadata))
            except Exception as e:
                print(f"[METADATA STORE ERROR]: Failed to load metadata: {e}")
                self.metadata = {}
                self.next_faiss_id = 0
        else:
            self.metadata = {}
            self.next_faiss_id = 0

        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    mdata = json.load(f)
                    self.manifest = IndexingManifest(**mdata)
            except Exception as e:
                print(f"[MANIFEST STORE ERROR]: Failed to load manifest: {e}")
                self.manifest = IndexingManifest()

    def save(self):
        try:
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump({
                    "chunks": {str(k): v for k, v in self.metadata.items()},
                    "next_faiss_id": self.next_faiss_id
                }, f, indent=2)

            with open(self.manifest_file, "w", encoding="utf-8") as f:
                json.dump(self.manifest.model_dump(), f, indent=2)
        except Exception as e:
            print(f"[METADATA STORE ERROR]: Failed to save metadata/manifest: {e}")

    def add_chunks(self, chunks: List[Chunk]) -> List[int]:
        assigned_ids = []
        doc_path = ""
        doc_hash = ""

        for chunk in chunks:
            faiss_id = self.next_faiss_id
            self.next_faiss_id += 1
            assigned_ids.append(faiss_id)

            self.metadata[faiss_id] = {
                "text": chunk.text,
                "metadata": chunk.metadata.model_dump()
            }
            doc_path = chunk.metadata.source_path
            doc_hash = chunk.metadata.document_hash

        if doc_path:
            self.manifest.documents[doc_path] = {
                "document_hash": doc_hash,
                "faiss_ids": assigned_ids,
                "chunk_count": len(chunks),
                "modified_at": time.time()
            }
            self.manifest.total_chunks = len(self.metadata)
            self.manifest.last_updated = time.time()

        self.save()
        return assigned_ids

    def remove_document(self, doc_path: str) -> List[int]:
        doc_info = self.manifest.documents.get(doc_path)
        if not doc_info:
            return []

        faiss_ids_to_remove = doc_info.get("faiss_ids", [])
        for fid in faiss_ids_to_remove:
            self.metadata.pop(fid, None)

        del self.manifest.documents[doc_path]
        self.manifest.total_chunks = len(self.metadata)
        self.manifest.last_updated = time.time()

        self.save()
        return faiss_ids_to_remove

    def get_chunk(self, faiss_id: int) -> Optional[Dict[str, Any]]:
        return self.metadata.get(faiss_id)

    def get_doc_info(self, doc_path: str) -> Optional[Dict[str, Any]]:
        return self.manifest.documents.get(doc_path)

    def clear(self):
        self.metadata = {}
        self.next_faiss_id = 0
        self.manifest = IndexingManifest()
        if self.metadata_file.exists():
            try: os.remove(self.metadata_file)
            except Exception: pass
        if self.manifest_file.exists():
            try: os.remove(self.manifest_file)
            except Exception: pass

metadata_store = MetadataStore()
