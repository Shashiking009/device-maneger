import time
from typing import Tuple, Optional
from voice.config import WAKE_WORD_ALIASES, WAKE_WORD_COOLDOWN

class WakeWordDetector:
    """
    Lightweight local wake word detector monitoring for 'Hey Spidy'.
    Normalizes phonetic variations ("hey spidey", "a spider", "hey spider") cleanly.
    """
    def __init__(self, cooldown: float = WAKE_WORD_COOLDOWN):
        self.cooldown = cooldown
        self.last_detection_time = 0.0

    def normalize_wake_text(self, text: str) -> str:
        if not text:
            return ""
        lower = text.lower().strip()
        for alias in WAKE_WORD_ALIASES:
            if alias in lower:
                return lower.replace(alias, "hey spidy").strip()
        return lower

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
        if not text:
            return ""
        lower_text = text.lower().strip()
        for alias in WAKE_WORD_ALIASES:
            if alias in lower_text:
                idx = lower_text.find(alias)
                cmd_part = text[idx + len(alias):].strip()
                cmd_part = cmd_part.lstrip(",.:;?! ")
                return cmd_part
        return text.strip()

wake_word_detector = WakeWordDetector()
