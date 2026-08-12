# 🛡️ SPIDY AI v1.0.0 — STABLE RUNTIME & RESTORE POINT

**Release Version:** v1.0.0-stable  
**Architecture:** Single Owner FastAPI Backend & Pure HUD GUI Client  
**Mode:** Local / Offline-First  

---

## 1. Startup Procedure

Spidy AI v1.0.0 is configured for **100% automatic system-wide background startup**:

1. **Automatic Windows Boot**:
   - **Startup VBS**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Spidy_DeviceManager_Startup.vbs`
   - **Registry Run Key**: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SpidyAI`
   - Launches `start_spidy.bat` in hidden mode (`0`) on Windows user login.

2. **Manual Startup via CMD**:
   ```cmd
   cd /d "C:\Users\sasi vardhan.P\myname\device_manager" && start_spidy.bat
   ```

---

## 2. Single Owner Architecture

```text
                        STARTUP CONTROLLER
                     (start_spidy.bat / VBS)
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
        HEALTH CHECK 127.0.0.1:8088       SINGLETON MUTEX LOCK
                 │                             │
     ┌───────────┴───────────┐                 │
     │                       │                 │
 [IF HEALTHY]           [IF NOT RUNNING]       │
 Reuse existing server   Launch FastAPI server ◄─
         │                   │
         │             FastAPI Startup Event
         │                   │
         │             SINGLE VoiceManager Owner
         │             SINGLE Orchestrator Owner
         │                   │
         └─────────┬─────────┘
                   │
                   ▼
              HUD CLIENT
     (Pure GUI - Connects to 127.0.0.1:8088 via WS)
```

### Process Lifecycles & Ports
- **FastAPI Server Process (`server.py`)**: Owns `127.0.0.1:8088`, `SpidyOrchestrator`, `VoiceManager`, `MemoryService`, `RAGService`, `Telemetry`, and `WebSocket EventBus`.
- **Cyber HUD Process (`spidy_hud.py`)**: Pure Tkinter GUI client connecting to `http://127.0.0.1:8088/health` and `ws://127.0.0.1:8088/ws/spidy`.
- **Singleton Guard (`core/singleton_lock.py`)**: Cross-process mutex preventing duplicate server instances and eliminating `WinError 10048`.

---

## 3. Verified System Services

| Service | Port / Protocol | Status | Description |
|---|---|---|---|
| **FastAPI** | `127.0.0.1:8088` | `ONLINE` | Authoritative backend server |
| **Voice Manager** | System Mic / SAPI5 | `ACTIVE` | System-wide background listening loop |
| **Microphone** | Audio Input | `CALIBRATED` | High sensitivity (`AUDIO_ENERGY_THRESHOLD = 120`) |
| **Wake Word** | Offline Matching | `ACTIVE` | Normalizes *"hey spidy"*, *"hey spidey"*, *"a spider"* |
| **Qwen3 SLM** | `127.0.0.1:11434` | `ONLINE` | Local Qwen3 1.7B language model |
| **FAISS Vector Store** | Persistent FAISS | `READY` | Grounded local document retrieval |
| **Memory Engine** | SQLite DB | `HEALTHY` | Persistent local context and preferences |
| **Cyber HUD** | WebSocket `/ws/spidy` | `CONNECTED` | Real-time desktop status overlay |

---

## 4. Voice Commands Quick Reference

Wake Phrase: **"Hey Spidy"** (Responds aloud: *"Yes boss, what can I do for you?"*)

- **Applications**: *"Hey Spidy, open Chrome"*, *"open Calculator"*, *"open VS Code"*, *"open Notepad"*, *"open File Explorer"*, *"close Calculator"*
- **Folders & Files**: *"Hey Spidy, open Downloads"*, *"open Documents"*, *"create folder AI Project"*
- **Window Controls**: *"Hey Spidy, minimize window"*, *"maximize window"*, *"show desktop"*
- **System & Volume**: *"Hey Spidy, increase volume"*, *"mute"*, *"unmute"*, *"how is my laptop?"*, *"are you working?"*
- **Voice Typing**: *"Hey Spidy, type Hello World"*, *"select all"*, *"copy"*, *"paste"*
- **AI Questions**: *"Hey Spidy, what is machine learning?"*

---

## 5. Recovery & Troubleshooting Procedure

If backend connection drops or Windows updates interrupt services:

1. **Check Server Health**:
   ```cmd
   python -c "import requests; print(requests.get('http://127.0.0.1:8088/health').json())"
   ```
2. **Restart Spidy Stack**:
   ```cmd
   python -c "import psutil; [p.terminate() for p in psutil.process_iter(['name', 'cmdline']) if 'uvicorn' in ' '.join(p.info['cmdline'] or [])]"
   cd /d "C:\Users\sasi vardhan.P\myname\device_manager" && start_spidy.bat
   ```
3. **Verify HUD Reconnection**:
   The Cyber HUD automatically reconnects via WebSocket as soon as the server health is restored.
