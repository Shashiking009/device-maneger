import time
import speech_recognition as sr
from typing import Tuple, Optional
from voice.config import WAKE_WORD_ALIASES, WAKE_WORD_COOLDOWN, AUDIO_ENERGY_THRESHOLD

class WakeWordDetector:
    """
    Lightweight local wake word detector monitoring for 'Hey Spidy'.
    100% Offline operation with false-activation cooldown protection.
    """
    def __init__(self, cooldown: float = WAKE_WORD_COOLDOWN):
        self.cooldown = cooldown
        self.last_detection_time = 0.0

    def is_wake_phrase(self, text: str) -> bool:
        if not text:
            return False

        now = time.time()
        if (now - self.last_detection_time) < self.cooldown:
            return False

        lower_text = text.lower().strip()
        for alias in WAKE_WORD_ALIASES:
            if alias in lower_text:
                self.last_detection_time = now
                return True
        return False

    def extract_command_after_wake(self, text: str) -> str:
        lower_text = text.lower().strip()
        for alias in WAKE_WORD_ALIASES:
            if alias in lower_text:
                idx = lower_text.find(alias)
                cmd_part = text[idx + len(alias):].strip()
                # Remove leading punctuation
                cmd_part = cmd_part.lstrip(",.:;?! ")
                return cmd_part
        return text.strip()

wake_word_detector = WakeWordDetector()
