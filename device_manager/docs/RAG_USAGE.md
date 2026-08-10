# 📖 SPIDY AI — LOCAL RAG USAGE GUIDE

## 1. REST API Endpoints

### Index Directory or File
- **POST** `/api/rag/index`
- **Request Body:**
```json
{
  "path": "C:\\Users\\sasi vardhan.P\\myname\\device_manager\\data\\documents"
}
```
- **Response:**
```json
{
  "status": "success",
  "directory": "...",
  "new_indexed": 5,
  "reindexed": 0,
  "skipped": 0,
  "deleted": 0,
  "chunks_added": 5,
  "total_chunks_in_db": 5,
  "time_ms": 142.5
}
```

### Semantic Search & Grounded Answer Query
- **POST** `/api/rag/query`
- **Request Body:**
```json
{
  "query": "What model does my project use?",
  "top_k": 5
}
```
- **Response:**
```json
{
  "success": true,
  "answer": "According to your project plan, the application uses Qwen3:1.7b as its local language model.\n\nSources:\n- project.md",
  "sources": ["project.md"],
  "query_time_ms": 1250.4
}
```

### Remove Document
- **DELETE** `/api/rag/document`
- **Request Body:**
```json
{
  "path": "C:\\Users\\sasi vardhan.P\\myname\\device_manager\\data\\documents\\notes.txt"
}
```

### Clear RAG Database
- **POST** `/api/rag/clear`

### RAG Database Status
- **GET** `/api/rag/status`
- **Response:**
```json
{
  "ready": true,
  "status": "READY",
  "documents_count": 5,
  "chunks_count": 5,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "vector_store": "FAISS (IndexFlatIP + IndexIDMap2)",
  "persistent": true
}
```

---

## 2. Voice & Natural Language Commands
You can query your indexed local documents directly via Spidy Voice HUD or Chat Interface:
- *"Hey Spidy, what does my project plan say about Qwen3?"*
- *"Hey Spidy, search my documents for hardware requirements."*
