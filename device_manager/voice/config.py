import os

# Voice Settings
WAKE_WORD = "Hey Spidy"
WAKE_WORD_ALIASES = [
    "hey spidy", "hi spidy", "spidy", "spidey", "spider", "speedy", "ok spidy",
    "hey spidey", "hey spider", "hey speedy", "hey sweetie", "hey spotify", "hey petey",
    "a spidy", "a spidey", "hi spidey", "ok spidey"
]
WAKE_WORD_SENSITIVITY = 0.7
WAKE_WORD_COOLDOWN = 1.0  # seconds between wake activations

# Speech Recognition & Listening Parameters
LISTEN_TIMEOUT = 6.0       # seconds to wait for speech start
MAX_LISTEN_SECONDS = 10.0  # max phrase duration
AUDIO_ENERGY_THRESHOLD = 120  # High sensitivity for laptop microphones
PAUSE_THRESHOLD = 0.5

# Text-To-Speech Parameters
TTS_ENABLED = True
TTS_RATE = 0              # -10 to +10 SAPI5 rate
TTS_VOLUME = 100          # 0 to 100
MAX_SPOKEN_CHARS = 250    # Concise spoken responses
STOP_PHRASES = ["stop", "stop spidy", "quiet", "shut up", "hush", "pause"]

WAKE_RESPONSES = [
    "Yes boss, what can I do for you?",
    "Yes boss, I'm listening.",
    "At your service, boss.",
    "Yes boss, how can I help you today?"
]
