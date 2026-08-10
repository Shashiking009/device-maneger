# Spidy AI Project Overview

Spidy AI is an edge-computing, privacy-first, on-device AI assistant developed for Windows.
The system uses the **Qwen3:1.7b** Small Language Model (SLM) running locally on Ollama C++ runtime at `http://127.0.0.1:11434`.
FastAPI serves endpoints locally on port `8088`.
The local vector database uses **FAISS** with **Sentence-Transformers** (`all-MiniLM-L6-v2`) for offline document search.
