# 🕷️ SPIDY AI — PHASE-BY-PHASE IMPLEMENTATION ROADMAP

**Document Version:** 1.0.0  
**Project:** Device Manager — Spidy AI  
**Target Repository:** [https://github.com/Shashiking009/device-maneger](https://github.com/Shashiking009/device-maneger)

---

## 🎯 Implementation Strategy & Guidelines

To ensure maximum stability and preserve all working features:
1. **Preserve Working Code:** Do not refactor functional code unnecessarily.
2. **Incremental Execution:** Execute phases sequentially with verification checks after each phase.
3. **Zero Interruption:** Ensure FastAPI server (`port 8088`), Ollama (`qwen3:1.7b`), and Spidy HUD remain fully functional.

---

## 📌 Phase 0: Repository Audit & Architecture Planning (Current Phase)

- [x] Complete comprehensive audit of all Python scripts, static assets, database schemas, and startup batch files.
- [x] Document target architecture diagram and identify working vs duplicate vs missing features.
- [x] Create `docs/ARCHITECTURE_AUDIT.md`.
- [x] Create `docs/IMPLEMENTATION_ROADMAP.md`.
- [x] Verify current application startup health and port responsiveness.

---

## 📌 Phase 1: Codebase Consolidation & Configuration Cleanup

**Objective:** Clean up duplicate scripts, unify port configurations, remove hardcoded user paths, and add top-level `requirements.txt`.

### Action Items:
1. **Unify Server Port Configuration:**
   - Standardize default port to `8088` across `server.py`, `start_spidy.bat`, and `spidy_hud.py`.
2. **Remove Hardcoded System Paths:**
   - Replace explicit `C:\Users\sasi vardhan.P\...` paths with dynamic `os.path.expanduser("~")` or relative workspace paths.
3. **Deprecate & Archive Duplicate Scripts:**
   - Move legacy/duplicate listeners (`spidy_listener.py`, `spidy_jarvis_hud.py`), batch files (`start_spidy_background.bat`, `start_spidy_jarvis.bat`), and startup installers (`setup_startup.py`) into an `archive/` folder.
4. **Create Root `requirements.txt`:**
   - Explicitly list dependencies: `fastapi`, `uvicorn`, `requests`, `psutil`, `pydantic`, `speechrecognition`, `pyaudio`, `pyautogui`, `sentence-transformers`, `faiss-cpu`, `pywin32`.

---

## 📌 Phase 2: Centralized Orchestrator & AI Router Module

**Objective:** Introduce an explicit `orchestrator.py` module matching the target system diagram.

```
                          ┌──────────────────┐
                          │   SPIDY ROUTER   │
                          └────────┬─────────┘
                                   │
       ┌──────────────┬────────────┼───────────┬──────────────┐
       ▼              ▼            ▼           ▼              ▼
  OS ACTION     SYSTEM INFO    LOCAL RAG   SLM AI Q&A      FALLBACK
 (Apps/Power)    (psutil)      (Docs)      (Ollama)        (Error)
```

### Action Items:
1. **Implement `orchestrator.py`:**
   - Define an explicit intent classification pipeline.
   - Route incoming commands to appropriate sub-engines (Windows Automation, RAG Search, System Metrics, or Qwen3 SLM).
2. **Refactor Endpoint Ingestion:**
   - Connect `/api/voice/command` and `/api/chat` directly through `orchestrator.py`.

---

## 📌 Phase 3: RAG Engine Upgrade & Persistent Embeddings

**Objective:** Upgrade in-memory TF-IDF search to persistent local vector embeddings.

### Action Items:
1. **Add Local FAISS Vector Storage:**
   - Persist document chunk embeddings to disk (`vector_store.index`).
2. **Auto-Reload on Startup:**
   - Ensure document chunks stored in SQLite are re-loaded into FAISS index automatically on server boot.

---

## 📌 Phase 4: Voice Engine & Windows Automation Hardening

**Objective:** Enhance microphone capture reliability and keyboard/mouse automation safety.

### Action Items:
1. **Audio Capture Recovery:** Add automatic retries and device fallback if microphone input is interrupted.
2. **Process Termination Safety:** Enhance `close_application_process` to target specific user applications without killing system critical processes.

---

## 📌 Phase 5: Spidy HUD & UI Integration Polish

**Objective:** Polish the floating transparent desktop HUD and synchronize state with the Web UI.

### Action Items:
1. **HUD Status Feedback:** Ensure smooth animation transitions for `SPIDY ONLINE`, `WAKE DETECTED`, `THINKING...`, and `EXECUTED`.
2. **Web Dashboard Telemetry Sync:** Ensure live CPU/Memory telemetry cards update seamlessly in `static/index.html`.

---

## 📌 Phase 6: End-to-End Testing & Verification

**Objective:** Validate full system startup and functionality after all phases.

### Verification Checklist:
- [ ] Verify `start_spidy.bat` boots FastAPI on port 8088 and Spidy HUD.
- [ ] Verify wake word `"Hey Spidy"` triggers instant execution.
- [ ] Verify app launch (`calc.exe`, `notepad.exe`) and termination (`close calculator`).
- [ ] Verify Qwen3 SLM chat streaming and local document RAG.
- [ ] Confirm clean git repository status.
