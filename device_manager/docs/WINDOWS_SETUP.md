# 💻 SPIDY AI v1.0.0 — WINDOWS SETUP & TROUBLESHOOTING GUIDE

## 🚀 Quick Launch via CMD

1. Open **Command Prompt (CMD)**.
2. Navigate to your repository directory:
   ```cmd
   cd /d "C:\Users\sasi vardhan.P\myname\device_manager"
   ```
3. Run official launcher:
   ```cmd
   start_spidy.bat
   ```

---

## 🎙️ System-Wide Voice Operation

Spidy AI listens in the background for the wake phrase **"Hey Spidy"** regardless of which Windows application currently has focus (Chrome, VS Code, Notepad, File Explorer, PowerPoint, etc.).

### Windows Microphone Permissions
Ensure Windows allows background app access:
1. Open Windows **Settings** (`Win + I`).
2. Go to **Privacy & security** ➔ **Microphone**.
3. Set **Microphone access** to **ON**.
4. Set **Let desktop apps access your microphone** to **ON**.

---

## 🔧 Windows Troubleshooting Matrix

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Python is not installed"** | Python missing from system PATH | Reinstall Python 3.11+ and check *"Add Python to PATH"*. |
| **"Ollama is not running"** | Ollama service stopped | Start Ollama app or run `ollama serve` in CMD. |
| **"Qwen3 model not installed"** | `qwen3:1.7b` missing | Run `ollama pull qwen3:1.7b` in CMD. |
| **"Port 8088 already in use"** | Previous server instance open | Run `netstat -ano \| findstr 8088` and terminate pid, or rerun `start_spidy.bat`. |
| **Microphone not responding** | Muted or permission blocked | Verify microphone in Windows Sound settings and grant permissions. |
