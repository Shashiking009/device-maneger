# 🕷️ SPIDY AI — DESKTOP HUD ARCHITECTURE

## Overview
Spidy AI Phase 5 delivers a persistent, Jarvis-inspired desktop AI interface (`SpidyCyberHUD`). It functions as an unobtrusive, always-on-top, frameless desktop companion that visualizes real-time voice, AI processing, system telemetry, and command execution states driven by WebSocket event streams from the FastAPI backend.

---

## High-Level Architecture

```text
       Spidy Orchestrator & Voice Manager
                       │
                       ▼
            SpidyEventBus Publisher
                       │
                       │ WebSocket Broadcast (/ws/spidy)
                       ▼
              WebSocket Client Loop
                       │
                       ▼
           SpidyCyberHUD Interface (Tkinter)
  (Frameless, Always-on-Top, Position-Persistent)
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   Visual Rings   State Labels   System Telemetry
   (Pulse/Rotate) (LISTENING)    (CPU/RAM/Local)
```

---

## Architectural Guarantees
1. **Presentation Layer Only:** The HUD contains zero command-routing or OS execution logic (`os.system`, `subprocess.run`, `pyautogui`). It strictly presents backend events and sends user queries through `SpidyOrchestrator`.
2. **Single Source of Truth:** All states (`IDLE`, `LISTENING`, `PROCESSING`, `THINKING`, `EXECUTING`, `SPEAKING`, `ERROR`) are managed centrally by the backend `VoiceStateMachine` and `SpidyEventBus`.
3. **Automatic Reconnection:** The HUD maintains a WebSocket connection with exponential backoff (`1s, 2s, 4s, 8s, 16s`), gracefully transitioning to `OFFLINE` if the backend restarts.
4. **Position Persistence:** Window coordinates are saved to `data/hud_config.json` on drag release and restored automatically on system startup.
