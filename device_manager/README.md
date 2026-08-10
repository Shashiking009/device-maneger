# 🕷️ SPIDY AI v1.0.0 — PRIVACY-FIRST DESKTOP ASSISTANT

Spidy AI is an offline-first, Jarvis-inspired intelligent desktop assistant powered by local AI execution (`Qwen3 1.7B` SLM via Ollama), local FAISS vector search RAG, real-time voice speech recognition, SAPI5 text-to-speech synthesis, and a transparent Cyber Floating HUD display.

---

## 🌟 Key Features

- **100% Local AI & Privacy:** All language processing, embedding generation, vector search, and voice synthesis execute offline on your host machine.
- **Central Decision Orchestrator:** Single decision-making entry point (`SpidyOrchestrator`) ensuring zero direct shell/untrusted OS execution.
- **Jarvis-Style Desktop HUD:** Transparent, always-on-top floating cyber emblem visualising real-time voice and system states (`IDLE`, `LISTENING`, `THINKING`, `EXECUTING`, `SPEAKING`).
- **"Hey Spidy" Voice Assistant:** Offline wake-word detection, speech-to-text, and voice interruption (*"Stop"*, *"Quiet"*).
- **Persistent Local RAG:** Index `.txt`, `.md`, `.py`, `.json`, `.csv` files into a persistent local FAISS vector index with grounded Qwen3 answers.
- **Multi-Step Action Engine:** Parses and executes multi-action natural language commands (*"Open calculator and notepad"*) with strict risk classification and verification.
- **Local Memory Engine:** SQLite-backed user preference and fact store with automatic secret detection (`sk-`, API key shield) and pronoun reference resolution (*"Open my editor"* ➔ launches VS Code).

---

## 🛠️ Technology Stack

- **Core Backend:** Python 3.11+, FastAPI, Uvicorn, SQLite
- **AI SLM Engine:** Ollama (`qwen3:1.7b`)
- **Vector Search & RAG:** FAISS (`IndexFlatIP` + `IndexIDMap2`), Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Speech Subsystem:** SpeechRecognition, SAPI5 (Windows COM), PyAudio
- **Interface & Telemetry:** Tkinter Cyber HUD, WebSockets (`/ws/spidy`), `psutil`

---

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start Ollama & Pull Qwen3 Model:**
   ```bash
   ollama pull qwen3:1.7b
   ```
3. **Run Installer:**
   ```bash
   python install_spidy_software.py
   ```
4. **Launch Spidy AI:**
   ```bash
   python server.py
   ```

---

## 📖 Documentation
- [Architecture Overview](docs/FINAL_ARCHITECTURE.md)
- [Security Model](docs/SECURITY.md)
- [Privacy Policy](docs/PRIVACY.md)
- [Voice Commands Guide](docs/VOICE_COMMANDS.md)
- [Master Test Report](docs/FINAL_TEST_REPORT.md)
