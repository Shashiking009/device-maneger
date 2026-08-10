import re
from typing import Tuple, Dict, Any, Optional
from core.intent_models import Intent, IntentType, RiskLevel
from core.command_registry import APP_ALIASES, normalize_app_name
from ai.qwen_engine import qwen_engine
from voice_assistant import KNOWN_APPS, KNOWN_FOLDERS

class IntentRouter:
    """
    Hybrid Intent Classifier:
    1. Fast Deterministic Regex Matching (0ms latency, 0 CPU/LLM cost)
    2. Qwen3 SLM Fallback Classifier for natural language variations
    """
    def __init__(self):
        pass

    def classify_deterministic(self, clean_input: str) -> Optional[Intent]:
        cmd = clean_input.lower().strip()
        if not cmd:
            return None

        # 1. Volume & Audio Controls
        if "volume up" in cmd or "louder" in cmd:
            return Intent(name=IntentType.VOLUME_UP, confidence=1.0, parameters={"raw_cmd": "volume up"})
        if "volume down" in cmd or "lower volume" in cmd or "quiet" in cmd:
            return Intent(name=IntentType.VOLUME_DOWN, confidence=1.0, parameters={"raw_cmd": "volume down"})
        if "unmute" in cmd:
            return Intent(name=IntentType.UNMUTE, confidence=1.0, parameters={"raw_cmd": "unmute"})
        if "mute" in cmd:
            return Intent(name=IntentType.MUTE, confidence=1.0, parameters={"raw_cmd": "mute"})

        # 2. Lock & System Controls
        if "lock laptop" in cmd or "lock computer" in cmd or "lock screen" in cmd or cmd == "lock":
            return Intent(name=IntentType.LOCK_SYSTEM, confidence=1.0, risk_level=RiskLevel.MEDIUM, parameters={"raw_cmd": "lock laptop"})

        # 3. System Status
        if "system" in cmd and ("status" in cmd or "stats" in cmd or "health" in cmd or "diagnostics" in cmd):
            return Intent(name=IntentType.SYSTEM_STATUS, confidence=1.0)

        # 4. Keyboard Controls
        if "select all" in cmd:
            return Intent(name=IntentType.KEY_PRESS, target="ctrl+a", confidence=1.0, parameters={"raw_cmd": "select all"})
        if "copy" in cmd and "file" not in cmd and "folder" not in cmd:
            return Intent(name=IntentType.COPY, confidence=1.0, parameters={"raw_cmd": "copy"})
        if "paste" in cmd:
            return Intent(name=IntentType.PASTE, confidence=1.0, parameters={"raw_cmd": "paste"})
        
        type_match = re.search(r'^(?:type|write|say)\s+(.+)', cmd)
        if type_match:
            text_to_type = type_match.group(1).strip()
            return Intent(name=IntentType.TYPE_TEXT, target=text_to_type, confidence=1.0, parameters={"raw_cmd": cmd})

        if "press enter" in cmd or "hit enter" in cmd:
            return Intent(name=IntentType.KEY_PRESS, target="enter", confidence=1.0, parameters={"raw_cmd": "press enter"})
        if "press space" in cmd or "hit space" in cmd:
            return Intent(name=IntentType.KEY_PRESS, target="space", confidence=1.0, parameters={"raw_cmd": "press space"})

        # 5. App Closing Commands across APP_ALIASES & KNOWN_APPS
        for alias_key in set(list(APP_ALIASES.keys()) + list(KNOWN_APPS.keys())):
            if f"close {alias_key}" in cmd or f"kill {alias_key}" in cmd or f"exit {alias_key}" in cmd or f"terminate {alias_key}" in cmd:
                norm_app = normalize_app_name(alias_key)
                return Intent(name=IntentType.CLOSE_APPLICATION, target=norm_app, confidence=1.0)

        # 6. Folder Opening Commands
        for folder_key in KNOWN_FOLDERS.keys():
            if f"open {folder_key}" in cmd or f"show {folder_key}" in cmd:
                return Intent(name=IntentType.OPEN_FOLDER, target=folder_key, confidence=1.0)

        # 7. File Opening Commands
        open_file_match = re.search(r'^(?:open|launch|read|view)\s+(?:file|doc|document)\s+([a-zA-Z0-9_\-\.\s]+)', cmd)
        if open_file_match:
            target_file = open_file_match.group(1).strip()
            return Intent(name=IntentType.OPEN_FILE, target=target_file, confidence=1.0)

        # 8. App Opening Commands across APP_ALIASES & KNOWN_APPS
        for alias_key in set(list(APP_ALIASES.keys()) + list(KNOWN_APPS.keys())):
            if f"open {alias_key}" in cmd or f"launch {alias_key}" in cmd or f"start {alias_key}" in cmd or cmd == alias_key:
                norm_app = normalize_app_name(alias_key)
                return Intent(name=IntentType.OPEN_APPLICATION, target=norm_app, confidence=1.0)

        return None

    def route(self, user_input: str) -> Intent:
        # Normalize input & strip wake word
        clean_input = re.sub(r'^(hey|hi|hello|ok|okay)?\s*(spidy|spidey|spider)\s*', '', user_input.lower().strip()).strip()
        if not clean_input:
            clean_input = user_input.lower().strip()

        # Step 1: Fast Deterministic Match
        det_intent = self.classify_deterministic(clean_input)
        if det_intent:
            return det_intent

        # Step 2: Fallback to Qwen3 SLM Intent Classifier for natural language
        qwen_json = qwen_engine.classify_intent_with_qwen(clean_input)
        if qwen_json and isinstance(qwen_json, dict):
            name_str = qwen_json.get("name", "UNKNOWN").upper()
            target_str = qwen_json.get("target")
            confidence = float(qwen_json.get("confidence", 0.9))

            try:
                intent_enum = IntentType(name_str)
                if intent_enum != IntentType.UNKNOWN and intent_enum != IntentType.AI_QUESTION:
                    return Intent(
                        name=intent_enum,
                        target=target_str,
                        parameters=qwen_json.get("parameters", {}),
                        confidence=confidence
                    )
            except ValueError:
                pass

        # Step 3: Default to AI_QUESTION for general prompts
        return Intent(name=IntentType.AI_QUESTION, target=None, confidence=0.9)
