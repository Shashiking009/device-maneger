# 🕷️ Device Manager — Spidy AI

Privacy-First On-Device Small Language Model (SLM) Orchestrator & Hands-Free OS Voice Assistant.

---

## 🚀 Active Configuration & Entry Points

- **FastAPI Backend Server:** `http://127.0.0.1:8088`
- **Ollama Engine:** `http://127.0.0.1:11434`
- **SLM Model:** `qwen3:1.7b`
- **Active Desktop HUD:** `spidy_hud.py`
- **Active Startup Launcher:** `start_spidy.bat`
- **Active Installer:** `install_spidy_software.py`

---

## 📂 Archival Structure

Legacy prototype listener variants and batch scripts have been safely moved to `archive/`:
- `archive/legacy_hud/` (`spidy_listener.py`, `spidy_jarvis_hud.py`)
- `archive/legacy_launchers/` (`start_spidy_background.bat`, `start_spidy_jarvis.bat`)
- `archive/legacy_startup/` (`setup_startup.py`)

---

## 🏃 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the full application (FastAPI server + Spidy Cyber HUD):
   ```cmd
   start_spidy.bat
   ```

3. Generate desktop shortcut and Windows boot startup script:
   ```bash
   python install_spidy_software.py
   ```
