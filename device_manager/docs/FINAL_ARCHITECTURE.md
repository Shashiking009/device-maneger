# 🕷️ SPIDY AI — FINAL SYSTEM ARCHITECTURE

## Complete System Blueprint

```text
                    SPIDY AI v1.0.0
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
      Voice               Chat               HUD
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    FastAPI Backend
                    (127.0.0.1:8088)
                           │
                           ▼
                   SPIDY ORCHESTRATOR
                (Single Entry Authority)
                           │
       ┌───────────────────┼──────────────────┐
       ▼                   ▼                  ▼
    Memory                RAG           Intent Router
       │                   │                  │
       └───────────────────┼──────────────────┘
                           ▼
                    Action Planner
                           │
                           ▼
                  Security Validator
                           │
                           ▼
                    Action Executor
                           │
                           ▼
                     Verification
                           │
                     Event Bus
                      /        \
                     ▼          ▼
                    HUD        TTS
```

---

## Component Separation Guarantees
1. **Single Entry Point Authority:** All text, voice, REST, and WebSocket commands flow strictly through `SpidyOrchestrator`. No sub-module can bypass security validation or execute arbitrary shell code.
2. **Data vs Instruction Isolation:** Both RAG document contents and stored user memories are treated strictly as inert data strings. They cannot contain executable commands.
3. **Event-Driven Visual HUD:** `SpidyCyberHUD` receives asynchronous state events via WebSocket `/ws/spidy` without polling components.
