# 🎙️ SPIDY AI — VOICE ASSISTANT & WAKE-WORD ARCHITECTURE

## Overview
Spidy AI Phase 4 implements a 100% offline, privacy-first local voice assistant subsystem. The architecture continuously monitors microphone audio locally for the wake phrase **"Hey Spidy"**, transitions through a formal state machine, captures speech-to-text input, delegates intent resolution strictly to `SpidyOrchestrator`, and speaks concise responses via Windows SAPI5 Text-To-Speech with full voice interruption support.

---

## Target Pipeline

```text
               MICROPHONE AUDIO (Local)
                          │
                          ▼
            LIGHTWEIGHT WAKE-WORD DETECTOR
                    ("Hey Spidy")
                          │
                          ▼
                VOICE STATE MACHINE
      (IDLE → LISTENING → PROCESSING → EXECUTING → SPEAKING)
                          │
                          ▼
                 SPEECH-TO-TEXT (STT)
                          │
                          ▼
                SPIDY ORCHESTRATOR
                (Single Entry Point)
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    COMMAND REGISTRY    QWEN3 SLM    LOCAL RAG (FAISS)
          │               │               │
          └───────────────┬───────────────┘
                          │
                          ▼
                TEXT-TO-SPEECH (TTS)
              (SAPI5 + Interruption)
                          │
                          ▼
                SPIDY CYBER HUD DISPLAY
```

---

## Architectural Principles
1. **Voice Layer Contains Zero Command Routing:** The voice subsystem strictly converts `Audio → Text` and `Text → Audio`. All intent classification and command execution are performed exclusively by `SpidyOrchestrator`.
2. **100% Offline Privacy:** Microphone audio is never streamed to cloud servers. All wake-word detection, speech recognition, and speech synthesis run locally on the host machine.
3. **Voice Interruption:** Saying *"Stop"*, *"Quiet"*, or *"Stop Spidy"* immediately halts active SAPI5 speech synthesis and returns Spidy to `IDLE` state.
4. **Concise Spoken Response Policy:** Spidy speaks concise summaries (max 250 characters) while displaying complete full text answers on the Cyber HUD & Web Dashboard.

---

## Core Components
- **`voice/config.py`**: Voice parameters (`WAKE_WORD="Hey Spidy"`, `LISTEN_TIMEOUT=6.0`, `MAX_LISTEN_SECONDS=10.0`, `MAX_SPOKEN_CHARS=250`, `STOP_PHRASES`).
- **`voice/models.py`**: `VoiceState` Enum (`IDLE`, `LISTENING`, `PROCESSING`, `EXECUTING`, `SPEAKING`, `ERROR`, `STOPPED`) and `VoiceEvent` model.
- **`voice/voice_state.py`**: State machine managing valid state transitions and broadcasting events to HUD and API subscribers.
- **`voice/audio_manager.py`**: Microphone device availability detection and single-audio-session locking.
- **`voice/wake_word.py`**: Local wake-word detector with sensitivity tuning, false-activation cooldown, and command string extraction.
- **`voice/speech_to_text.py`**: Speech-to-Text engine with listen timeouts and phrase limits.
- **`voice/text_to_speech.py`**: Non-blocking SAPI5 TTS engine with thread-safe COM initialization and interruption support.
- **`voice/voice_manager.py`**: Central orchestrator coordinating microphone capture, STT, `SpidyOrchestrator`, and TTS playback.
