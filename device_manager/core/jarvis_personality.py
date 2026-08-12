import random
from typing import Optional, Dict, Any

class JarvisPersonality:
    """
    JARVIS Persona Response Generator.
    Produces natural, professional, respectful, and slightly witty voice responses.
    Uses 'boss' naturally without repetitive boilerplate.
    """
    def __init__(self):
        self.style = "jarvis"

    def format_response(self, intent_name: str, raw_message: str, success: bool = True) -> str:
        if not raw_message:
            return "Done, boss." if success else "I encountered an issue, boss."

        clean_msg = raw_message.strip()

        # Transform robotic responses
        if "command executed" in clean_msg.lower() or "successfully executed" in clean_msg.lower():
            return "Done, boss."

        # Preserve status/error details naturally
        if "not running" in clean_msg.lower() or "not found" in clean_msg.lower() or "couldn't find" in clean_msg.lower():
            if not clean_msg.endswith(", boss.") and not clean_msg.endswith("boss"):
                return f"{clean_msg.rstrip('. ')}, boss."
            return clean_msg

        if intent_name == "OPEN_APPLICATION":
            if "opening" in clean_msg.lower():
                return clean_msg
            return f"Opening {clean_msg}, boss."

        if intent_name == "CLOSE_APPLICATION":
            if "closing" in clean_msg.lower() or "closed" in clean_msg.lower():
                return clean_msg
            return f"Closed {clean_msg}, boss."

        if intent_name == "VOLUME_UP":
            return "Volume increased, boss."

        if intent_name == "VOLUME_DOWN":
            return "Volume decreased, boss."

        if intent_name == "MUTE":
            return "Muted, boss."

        if intent_name == "UNMUTE":
            return "Unmuted, boss."

        if intent_name == "TYPE_TEXT":
            return "Typed, boss."

        if intent_name == "SYSTEM_STATUS":
            return clean_msg

        return clean_msg

    def get_greeting(self) -> str:
        greetings = [
            "Yes boss, what can I do for you?",
            "Yes boss, I'm listening.",
            "At your service, boss.",
            "Standing by, boss."
        ]
        return random.choice(greetings)

jarvis_personality = JarvisPersonality()
