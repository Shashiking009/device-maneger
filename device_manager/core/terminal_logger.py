import sys
import time
from typing import Optional, Any, Dict

class TerminalLogger:
    """
    High-Visibility Terminal Conversation Logger for Spidy AI.
    Prints structured, readable pipeline steps for debugging user voice commands in Windows CMD.
    Uses ASCII indicators to prevent Windows cp1252 encoding crashes.
    """
    def __init__(self):
        self.enabled = True

    def _timestamp(self) -> str:
        return time.strftime("[%H:%M:%S]")

    def log_user(self, text: str):
        print("\n" + "=" * 60)
        print(f"{self._timestamp()} USER")
        print(f"> {text}")

    def log_wake(self, phrase: str = "hey spidy", detected: bool = True):
        status = "[OK]" if detected else "[FAILED]"
        print(f"\n{self._timestamp()} WAKE")
        print(f"{status} \"{phrase}\" detected")

    def log_voice_auth(self, authorized: bool, confidence: float = 1.0):
        status = "[OK] Authorized speaker" if authorized else "[DENIED] Unauthorized speaker — command ignored"
        print(f"\n{self._timestamp()} VOICE AUTH")
        print(f"{status}")
        print(f"Confidence: {confidence:.2f}")

    def log_command(self, cmd: str):
        print(f"\n{self._timestamp()} COMMAND")
        print(f"> {cmd}")

    def log_intent(self, intent_name: str, confidence: float = 1.0):
        print(f"\n{self._timestamp()} INTENT")
        print(f"> {intent_name}")
        print(f"Confidence: {confidence:.2f}")

    def log_target(self, target: str):
        print(f"\n{self._timestamp()} TARGET")
        print(f"> {target}")

    def log_action(self, action_name: str):
        print(f"\n{self._timestamp()} ACTION")
        print(f"> {action_name}")

    def log_result(self, success: bool, message: Optional[str] = None):
        status = "[OK] SUCCESS" if success else "[DENIED] FAILED / REJECTED"
        print(f"\n{self._timestamp()} RESULT")
        print(f"{status}")
        if message:
            print(f"Details: {message}")

    def log_model(self, model_name: str = "Qwen3 1.7B"):
        print(f"\n{self._timestamp()} MODEL")
        print(f"> {model_name}")

    def log_spidy(self, response_text: str):
        print(f"\n{self._timestamp()} SPIDY")
        print(f"> {response_text}")
        print("=" * 60 + "\n")

    def log_error(self, err_msg: str):
        print(f"\n{self._timestamp()} ERROR")
        print(f"[ERROR] {err_msg}")
        print("=" * 60 + "\n")

terminal_logger = TerminalLogger()
