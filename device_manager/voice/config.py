import os

# Voice Settings
WAKE_WORD = "Hey Spidy"
WAKE_WORD_ALIASES = ["hey spidy", "hi spidy", "spidy", "spidey", "spider", "speedy", "ok spidy"]
WAKE_WORD_SENSITIVITY = 0.7
WAKE_WORD_COOLDOWN = 2.0  # seconds between wake activations

# Speech Recognition & Listening Parameters
LISTEN_TIMEOUT = 6.0       # seconds to wait for speech start
MAX_LISTEN_SECONDS = 10.0  # max phrase duration
AUDIO_ENERGY_THRESHOLD = 250
PAUSE_THRESHOLD = 0.6

# Text-To-Speech Parameters
TTS_ENABLED = True
TTS_RATE = 0              # -10 to +10 SAPI5 rate
TTS_VOLUME = 100          # 0 to 100
MAX_SPOKEN_CHARS = 250    # Concise spoken responses
STOP_PHRASES = ["stop", "stop spidy", "quiet", "shut up", "hush", "pause"]
