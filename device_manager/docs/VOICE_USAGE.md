# 📖 SPIDY AI — VOICE ASSISTANT USAGE GUIDE

## 1. Natural Voice Commands

Activate Spidy by speaking the wake phrase **"Hey Spidy"**:

### Application Control
- *"Hey Spidy, open calculator"*
- *"Hey Spidy, close notepad"*
- *"Hey Spidy, open vs code"*

### Volume & Audio Control
- *"Hey Spidy, volume up"*
- *"Hey Spidy, volume down"*
- *"Hey Spidy, mute"*

### Voice Typing
- *"Hey Spidy, type Hello World"*

### AI & Local RAG Questions
- *"Hey Spidy, what is machine learning?"*
- *"Hey Spidy, what does my project plan say about Qwen3?"*

### Voice Interruption
While Spidy is speaking, say:
- *"Stop"*
- *"Quiet"*
- *"Stop Spidy"*

---

## 2. REST API Voice Endpoints

### Get Voice State
- **GET** `/api/voice/status`
- **Response:**
```json
{
  "state": "IDLE",
  "is_speaking": false
}
```

### Stop Active Speech Synthesis
- **POST** `/api/voice/stop`

### Send Voice Text Command Directly
- **POST** `/api/voice/command`
- **Request Body:**
```json
{
  "command": "hey spidy open calculator"
}
```
