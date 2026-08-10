# 🕷️ SPIDY AI / DEVICE MANAGER — ARCHITECTURE AUDIT

**Document Version:** 1.0.0  
**Audit Date:** August 10, 2026  
**Target Repository:** [https://github.com/Shashiking009/device-maneger](https://github.com/Shashiking009/device-maneger)

---

## 1. Executive Summary

This document presents a comprehensive technical audit of the **Device Manager — Spidy AI** codebase. The repository contains an active prototype of an on-device AI assistant and operating system voice orchestrator built using Python 3.11, FastAPI, SQLite, PyAutoGUI, SpeechRecognition, and local Ollama (`qwen3:1.7b`).

While the core functionality (voice activation, app opening/closing, local SLM chat, and floating HUD) is functional, the repository currently contains duplicate entry points, hardcoded user paths, port inconsistencies, and a basic TF-IDF in-memory retrieval implementation.

---

## 2. Target vs Current Architecture Comparison

### Target Architecture Diagram
```
                         🕷️ SPIDY AI
                              │
                    ┌─────────▼─────────┐
                    │  ORCHESTRATOR     │
                    │   / AI ROUTER     │
                    └─────────┬─────────┘
                              │
        ┌─────────────┬───────┼────────┬──────────────┐
        ▼             ▼       ▼        ▼              ▼
     QWEN3          VOICE    RAG      WINDOWS      SYSTEM
     LOCAL          ENGINE  ENGINE   AUTOMATION   TELEMETRY
        │             │       │        │              │
        └─────────────┴───────┼────────┴──────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   SPIDY HUD/UI    │
                    └───────────────────┘
```

### Current Architecture Assessment
Currently, intent routing is implicitly handled across `voice_assistant.py` (regex matching) and `spidy_hud.py` (voice capture thread), rather than through a dedicated, centralized **Orchestrator / AI Router** module.

---

## 3. Comprehensive File & Module Inventory

| File / Module | Responsibility / Role | Status | Audit Findings |
| :--- | :--- | :--- | :--- |
| `server.py` | FastAPI REST & SSE Streaming Server | Working | Port defaults to 8000 in `__main__`, but batch scripts & HUD query port 8088. High coupling with RAG and voice endpoints. |
| `database.py` | SQLite DB schema & CRUD operations | Working | Uses `device_manager.db`. Covers sessions, messages, documents, and settings. Clean implementation. |
| `rag_engine.py` | Document chunking & retrieval | Working (Basic) | Uses basic in-memory TF-IDF math. Lacks persistent vector embeddings (FAISS/Chroma). Rebuilds IDF on every doc addition. |
| `system_monitor.py` | System metrics collection (psutil) | Working | Provides CPU, Memory, Disk, and uptime stats cleanly. |
| `voice_assistant.py` | Voice intent parsing & app manager | Working | Maps processes (`calc.exe`, `notepad.exe`, `code`, etc.) and handles Regex matching for app/folder/file actions. |
| `voice_automation.py` | Windows UI & volume automation | Working | Uses `ctypes` for VK volume keys & `pyautogui` for voice typing & keypresses (`FAILSAFE = False`). |
| `spidy_hud.py` | Cyber Spidy Transparent Desktop HUD | Active | Current primary GUI HUD (`tkinter`). Captures mic input, updates HUD text, calls `/api/voice/command` & `/api/chat`. |
| `spidy_listener.py` | Standalone voice listener script | Legacy / Duplicate | Precursor to `spidy_hud.py`. Uses blocking TTS and PowerShell toasts. |
| `spidy_jarvis_hud.py` | Pre-rebrand HUD variant | Legacy / Duplicate | Contains JARVIS branding and synchronous SAPI TTS calls. Replaced by `spidy_hud.py`. |
| `install_spidy_software.py` | Desktop shortcut & startup generator | Working | Targets active Desktop (`WScript.Shell` SpecialFolders) and creates `start_spidy.bat` + `Spidy_DeviceManager_Startup.vbs`. |
| `setup_startup.py` | Older startup configuration script | Legacy / Duplicate | Replaced by `install_spidy_software.py`. |
| `start_spidy.bat` | Active launcher batch file | Working | Launches `uvicorn server:app --port 8088` and `spidy_hud.py`. |
| `start_spidy_background.bat` | Legacy launcher batch file | Legacy / Duplicate | Launches `spidy_listener.py`. |
| `start_spidy_jarvis.bat` | Legacy launcher batch file | Legacy / Duplicate | Launches `spidy_jarvis_hud.py`. |
| `static/` (`index.html`, `app.js`, `styles.css`) | Cyberpunk Obsidian Web Interface | Working | Full-featured frontend for Web chat, RAG document upload, and system metrics telemetry. |

---

## 4. Key Audit Findings & Categories

### 4.1 Working Features
- **FastAPI Core Server:** REST endpoints (`/api/system`, `/api/sessions`, `/api/documents`, `/api/voice/command`) and SSE token streaming (`/api/chat/stream`).
- **On-Device SLM Inference:** Connects to local Ollama runtime (`http://localhost:11434`) running `qwen3:1.7b`.
- **System-Wide Voice Intent Execution:** Opens/closes applications (`calculator`, `notepad`, `explorer`, `cmd`, `paint`, `chrome`, `edge`, `vs code`), adjusts volume, types text, and switches windows.
- **Floating Cyber Spidy HUD Widget:** Draggable, frameless `tkinter` overlay with transparent glass keying (`#010206`) and pulsing ring animation.
- **Auto-Start & Desktop Launcher:** Automatic Windows boot setup via `.vbs` launcher in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.

### 4.2 Broken & High-Risk Areas
1. **Port Mismatch:** `server.py` `if __name__ == "__main__":` runs on port `8000`, while `start_spidy.bat`, `spidy_hud.py`, and `install_spidy_software.py` expect port `8088`.
2. **Hardcoded User System Paths:** `voice_assistant.py` and `install_spidy_software.py` contain hardcoded user paths (`C:\Users\sasi vardhan.P\...`).
3. **In-Memory RAG Loss on Restart:** `RAGEngine` in `rag_engine.py` keeps chunks in memory (`self.chunks = []`). When the server restarts, document metadata exists in SQLite, but TF-IDF chunks are lost until re-indexed.

### 4.3 Duplicate Functionality
- **3 HUD / Listener Scripts:** `spidy_hud.py` (Active), `spidy_listener.py` (Deprecated), `spidy_jarvis_hud.py` (Deprecated).
- **3 Batch Files:** `start_spidy.bat` (Active), `start_spidy_background.bat` (Deprecated), `start_spidy_jarvis.bat` (Deprecated).
- **2 Startup Installers:** `install_spidy_software.py` (Active), `setup_startup.py` (Deprecated).

### 4.4 Missing Features
- **Centralized Orchestrator / AI Router Module (`orchestrator.py`):** Lacks explicit routing layer separating System Commands, RAG Queries, AI Reasoning, and Fallbacks.
- **Formal Dependency Specification (`requirements.txt`):** No top-level `requirements.txt` file exists in the repository root.
- **Vector Database Persistence:** Missing FAISS / Chroma disk persistence for document embeddings.

---

## 5. Recommended Refactored Architecture

```
                                🕷️ SPIDY AI
                                     │
                           ┌─────────▼─────────┐
                           │  ORCHESTRATOR     │  <-- New orchestrator.py
                           │   / AI ROUTER     │
                           └─────────┬─────────┘
                                     │
      ┌─────────────┬────────────────┼────────────────┬─────────────┐
      ▼             ▼                ▼                ▼             ▼
   qwen_slm.py   voice_engine.py  rag_engine.py    win_auto.py  sys_monitor.py
  (Ollama SLM)   (Mic Listener)   (FAISS Vector)  (PyAutoGUI)     (psutil)
      │             │                │                │             │
      └─────────────┴────────────────┼────────────────┴─────────────┘
                                     │
                           ┌─────────▼─────────┐
                           │   SPIDY HUD/UI    │  <-- spidy_hud.py + Web UI
                           └───────────────────┘
```

---

## 6. Verification Status

- **FastAPI Server (`http://127.0.0.1:8088`):** Verified operational.
- **Ollama Engine (`qwen3:1.7b`):** Verified online.
- **Spidy Cyber HUD (`spidy_hud.py`):** Verified operational in background.
