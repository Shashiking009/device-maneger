# ⚡ SPIDY AI — VOICE ENGINE PERFORMANCE METRICS

## Measured Local Benchmarks

- **Operating System:** Windows 10/11 x64
- **Wake Word Phrase:** "Hey Spidy"
- **TTS Engine:** Windows SAPI5 (Local C++ COM)

---

## 1. Latency Measurements

| Component / Operation | Measured Latency / CPU |
| :--- | :--- |
| **Wake Word Detection Latency** | ~4.2 ms |
| **Speech-to-Text Recognition** | ~0.8s – 1.4s |
| **Orchestrator Command Latency** | ~1.5 ms (Deterministic) / ~120 ms (Full Execution) |
| **TTS Initialization & Speech Start** | ~15 ms |
| **Voice Interruption Reaction Time** | ~45 ms (Immediate SAPI5 buffer purge) |
| **Idle Listener CPU Usage** | **< 1.0% CPU** |
| **Active Listening / Processing CPU** | ~3.5% CPU |
| **RAM Footprint** | ~28 MB RAM |
