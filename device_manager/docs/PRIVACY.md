# 🛡️ SPIDY AI — PRIVACY POLICY & LOCAL DATA MANAGEMENT

Spidy AI is designed to keep AI processing and stored assistant data local to your personal computer.

---

## Data Management & Local Storage

- **Local Storage Locations:**
  - Database & Memories: `device_manager/data/device_manager.db`
  - Local Vector Index: `device_manager/data/vector_store/index.faiss`
  - Uploaded Documents: `device_manager/data/uploaded_docs/`
  - Local Backups: `device_manager/data/backups/`
- **Deleting Memories:** Say *"Hey Spidy, forget my editor preference"* or *"Hey Spidy, forget everything"*.
- **Deleting RAG Documents:** Send `DELETE /api/rag/document` or delete files from `uploaded_docs`.
- **Zero Cloud Tracking:** Microphone audio, conversation logs, and document contents are never transmitted to third-party telemetry or cloud inference APIs.
