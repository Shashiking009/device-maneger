# 🧠 SPIDY AI — LOCAL RAG ARCHITECTURE

## Overview
Spidy AI Phase 3 implements an offline, privacy-first Retrieval-Augmented Generation (RAG) engine. The architecture indexes local text-based documents, stores 384-dimensional vector embeddings in a persistent FAISS index, and retrieves context for Qwen3 SLM grounded answers with deduplicated source citations.

---

## Target Pipeline

```text
                    LOCAL FILES (.txt, .md, .py, .json, .csv)
                                     │
                                     ▼
                              DOCUMENT LOADER (SHA-256 Hashing)
                                     │
                                     ▼
                               TEXT CLEANER
                                     │
                                     ▼
                       INTELLIGENT CHUNKER (600 chars, 120 overlap)
                                     │
                                     ▼
                           LOCAL EMBEDDING ENGINE
                      (sentence-transformers/all-MiniLM-L6-v2)
                                     │
                                     ▼
                         PERSISTENT VECTOR DB (FAISS IndexFlatIP + IndexIDMap2)
                                     │
                        ┌────────────┴────────────┐
                        │                         │
                  Vector Index              Metadata Store
                 (index.faiss)        (metadata.json & manifest.json)
                        │                         │
                        └────────────┬────────────┘
                                     │
                                     ▼
                            SEMANTIC RETRIEVER
                         (Cosine Score >= 0.15)
                                     │
                                     ▼
                           QWEN3 1.7B GROUNDED PROMPT
                                     │
                                     ▼
                         GROUNDED RESPONSE & CITATIONS
```

---

## Core Components

1. **`rag/loader.py`**: Reads `.txt`, `.md`, `.py`, `.json`, and `.csv` files. Computes SHA-256 content hashes, enforces size limits (`10MB`), and handles `utf-8`, `utf-8-sig`, and `latin-1` encodings. Excludes sensitive patterns (`.env`, `*.key`, `passwords*`).
2. **`rag/cleaner.py`**: Normalizes whitespace while preserving Markdown headers, Python indentation/comments, and JSON key/value pairs.
3. **`rag/chunker.py`**: Structure-aware chunking targeting ~600 characters per chunk with 120 character overlap. Attaches complete `ChunkMetadata` (`chunk_id`, `source_path`, `content_hash`, `document_hash`, timestamps).
4. **`rag/embeddings.py`**: Reusable singleton wrapper around `SentenceTransformer("all-MiniLM-L6-v2")`. Normalizes embeddings to unit length for exact Cosine Similarity under FAISS Inner Product (`IndexFlatIP`).
5. **`rag/vector_store.py`**: Persistent local FAISS database using `faiss.IndexFlatIP` wrapped in `faiss.IndexIDMap2`. Saves index to `device_manager/data/vector_store/index.faiss`.
6. **`rag/metadata_store.py`**: Synchronized JSON store (`metadata.json` & `manifest.json`) mapping integer FAISS IDs to chunk text, metadata, and document hashes.
7. **`rag/indexer.py`**: Incremental indexer. Compares document SHA-256 hashes against `manifest.json` to skip unchanged files, reindex modified files, index new files, and purge deleted files.
8. **`rag/retriever.py`**: Executes Cosine Similarity search with score threshold filtering (`RAG_MIN_SCORE = 0.15`). Prevents hallucinations by rejecting low-confidence matches.
9. **`rag/prompts.py`**: Dedicated RAG prompt forcing Qwen3 SLM to answer strictly using supplied document context and append source file citations.
10. **`rag/rag_engine.py`**: High-level unified service API (`query`, `index`, `reindex`, `remove`, `clear`, `status`).

---

## Security & Privacy
- **100% Offline Execution**: Zero network requests to OpenAI, Google, HuggingFace Inference, or cloud vector stores.
- **Path Sanitization & Sensitive File Exclusions**: Automatically excludes `.env`, SSH keys, credentials, and password files.
