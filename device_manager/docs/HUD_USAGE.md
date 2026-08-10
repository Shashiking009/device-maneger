# 📖 SPIDY AI — DESKTOP HUD USAGE GUIDE

## 1. Visual State Indicators

The Spidy Cyber HUD changes ring animations and neon colors based on active system state:

| Visual State | Color | Animation | Meaning |
| :--- | :--- | :--- | :--- |
| **OFFLINE** | Gray (`#6b7280`) | Static | FastAPI server offline or reconnecting |
| **IDLE** | Cyan (`#00f0ff`) | Slow Breathing Pulse | Spidy active & monitoring for "Hey Spidy" |
| **LISTENING** | Neon Pink (`#ff0055`) | Rapid Expanding Pulse | Microphone actively capturing speech |
| **PROCESSING** / **THINKING** | Amber (`#eab308`) | Rotating Hologram Ring | Qwen3 / RAG resolving query |
| **EXECUTING** | Emerald Green (`#10b981`) | Bright Directional Glow | OS action executing |
| **SPEAKING** | Cyber Purple (`#a855f7`) | Pulsating Waveform | SAPI5 TTS speaking response |
| **ERROR** | Crimson (`#ef4444`) | Flash Alert | Exception or device failure |

---

## 2. Desktop Controls
- **Drag HUD:** Click and hold anywhere on the HUD canvas to reposition it on screen. The position is automatically saved.
- **Close HUD:** Double click on the HUD canvas to close the desktop application.
