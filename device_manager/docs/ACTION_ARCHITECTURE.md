# 🕷️ SPIDY AI — ACTION PLANNING & EXECUTION ARCHITECTURE

## Overview
Spidy AI Phase 6 introduces a safe, intelligent action planning and computer control subsystem. The architecture allows Spidy to parse and execute multi-step natural language commands (e.g., *"Open calculator and notepad"*) while keeping `SpidyOrchestrator` as the central authority and maintaining strict security boundaries against arbitrary shell, file deletion, or unapproved executable execution.

---

## Action Pipeline Architecture

```text
                 USER REQUEST (Voice / Text)
                              │
                              ▼
                      SPIDY ORCHESTRATOR
                    (Single Central Entry)
                              │
                              ▼
                       ACTION PLANNER
                   (Deconstructs Steps)
                              │
                              ▼
                      ACTION VALIDATOR
             (Allowlist & Risk Classification)
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
       [ALLOWED ACTION]              [BLOCKED ACTION]
               │                             │
               ▼                             ▼
        ACTION EXECUTOR               HALT & EMIT ERROR
      (Sequential Loop)
               │
               ▼
      VERIFICATION & EVENTS
```

---

## Action Core Components
- **`actions/config.py`**: Central parameters (`ACTION_TIMEOUT=10.0`, `MAX_PLAN_STEPS=5`, `DRY_RUN=False`, `ALLOWED_APPLICATIONS`, `ALLOWED_KEYS`, `ALLOWED_HOTKEYS`).
- **`actions/models.py`**: Strongly typed `ActionType`, `RiskLevel` (`LOW`, `MEDIUM`, `HIGH`, `BLOCKED`), `ActionStatus`, `Action`, and `ActionPlan` models.
- **`actions/validator.py`**: Deterministic validator enforcing application allowlists, key whitelists, path traversal prevention (`../`), and shell injection pattern matching (`rm -rf`, `powershell`, `cmd.exe`).
- **`actions/planner.py`**: Intelligent deconstruction engine parsing multi-step queries into structured `ActionPlan` objects.
- **`actions/executor.py`**: Sequential execution engine with step-by-step verification, timeout enforcement, event broadcasting (`ACTION_PLAN_CREATED`, `ACTION_STARTED`, `ACTION_COMPLETED`), and plan cancellation support (`cancel_current_plan()`).
