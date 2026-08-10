# 🧠 SPIDY AI — LOCAL MEMORY & PERSONAL CONTEXT ARCHITECTURE

## Overview
Spidy AI Phase 7 implements a 100% offline local memory, conversation context, and personalization engine. It allows Spidy to remember user preferences, resolve pronoun references (*"open my editor"* ➔ launch VS Code), and maintain short-term and session context without cloud telemetry or external third-party storage.

---

## Memory Subsystem Pipeline

```text
               USER REQUEST (Voice / Text)
                            │
                            ▼
                    SPIDY ORCHESTRATOR
                  (Central Entry Point)
                            │
                            ▼
                     CONTEXT MANAGER
          (Pronoun & Reference Resolution)
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
  [EXPLICIT COMMAND]   [SECRET CHECK]    [ACTION ENGINE]
   ("Remember...")      (Rejects Keys)    (Executes App)
         │                  │                  │
         ▼                  ▼                  ▼
   MEMORY SERVICE      SQLITE DB         VERIFICATION
  (CRUD Operations)    (memories)
```

---

## Memory Categories
- **Short-Term Memory:** Pronoun & entity resolution within recent conversation turns.
- **Session Memory:** Active session context and message history bounded by `MAX_SESSION_MESSAGES` (10 turns).
- **Long-Term Memory:** Explicitly stored facts (*"User works on Device Manager project"*).
- **Preferences:** Key-value configuration (*"preferred_editor": "vscode"*, *"preferred_language": "python"*).

---

## Core Components
- **`memory/config.py`**: Parameters (`MEMORY_ENABLED=True`, `MAX_MEMORIES=200`, `MEMORY_CONFIDENCE_THRESHOLD=0.6`, `SECRET_PATTERNS`).
- **`memory/models.py`**: `MemoryCategory`, `MemorySource`, `Memory`, and `ConversationContext` Pydantic models.
- **`memory/secrets.py`**: Secret scanner protecting against storing API keys (`sk-`), Bearer tokens, private keys, or passwords.
- **`memory/storage.py`**: Thread-safe SQLite CRUD manager handling duplicate prevention and conflict updates.
- **`memory/context_manager.py`**: Reference resolver and context assembly engine.
- **`memory/memory_service.py`**: High-level natural language memory command parser (*"remember that..."*, *"what do you remember"*, *"forget that..."*).
