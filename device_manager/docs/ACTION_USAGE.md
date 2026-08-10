# 📖 SPIDY AI — MULTI-ACTION EXECUTION USAGE GUIDE

## 1. Natural Multi-Step Commands

Spidy AI can execute single commands or multi-step action plans:

### Multi-Step Application Launch
- *"Hey Spidy, open calculator and notepad"*
- *"Hey Spidy, open Chrome and then open VS Code"*

### Combined System Actions
- *"Hey Spidy, open calculator and volume up"*
- *"Hey Spidy, type Hello World and press enter"*

### Aborting Active Actions
While Spidy is executing a multi-step plan, say:
- *"Stop Spidy"*
- *"Cancel"*
- *"Abort"*

---

## 2. Dry-Run Testing Mode

Set `DRY_RUN = True` in `actions/config.py` to validate and simulate multi-step action plans without modifying the underlying operating system state.
