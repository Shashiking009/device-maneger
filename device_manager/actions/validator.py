import os
import re
from typing import Tuple, Optional
from actions.config import ALLOWED_APPLICATIONS, ALLOWED_KEYS, ALLOWED_HOTKEYS, MAX_TYPED_TEXT_LENGTH
from actions.models import Action, ActionType, RiskLevel, ActionStatus

FORBIDDEN_SHELL_PATTERNS = [
    r"\brm\s+-rf\b", r"\bdel\s+/f\b", r"\bformat\s+[a-z]:\b",
    r"\bpowershell\b", r"\bcmd\.exe\b", r"\breg\s+delete\b",
    r"\bnet\s+user\b", r"\bchmod\s+777\b", r"credentials", r"passwords"
]

class ActionValidator:
    """
    Deterministic Action Validator & Risk Classifier.
    Enforces application allowlists, path safety, key whitelists, and prompt injection defense.
    """
    def validate_action(self, action: Action) -> Tuple[bool, str, RiskLevel]:
        t = action.action_type
        p = action.parameters

        # Check for forbidden shell/malicious injection patterns in parameters
        param_str = str(p).lower()
        for pattern in FORBIDDEN_SHELL_PATTERNS:
            if re.search(pattern, param_str):
                return False, f"Action blocked due to security pattern match: '{pattern}'", RiskLevel.BLOCKED

        if t == ActionType.OPEN_APPLICATION:
            app_name = str(p.get("application", "")).lower().strip()
            if app_name not in ALLOWED_APPLICATIONS:
                return False, f"Application '{app_name}' is not in trusted application allowlist", RiskLevel.BLOCKED
            return True, f"Application '{app_name}' validated", RiskLevel.LOW

        elif t == ActionType.CLOSE_APPLICATION:
            app_name = str(p.get("application", "")).lower().strip()
            if app_name not in ALLOWED_APPLICATIONS:
                return False, f"Application '{app_name}' is not in trusted application allowlist", RiskLevel.BLOCKED
            return True, f"Close application '{app_name}' validated", RiskLevel.MEDIUM

        elif t == ActionType.TYPE_TEXT:
            text = str(p.get("text", ""))
            if len(text) > MAX_TYPED_TEXT_LENGTH:
                return False, f"Typed text length exceeds limit ({MAX_TYPED_TEXT_LENGTH} chars)", RiskLevel.BLOCKED
            return True, "Type text validated", RiskLevel.LOW

        elif t == ActionType.PRESS_KEY:
            key = str(p.get("key", "")).lower().strip()
            if key not in ALLOWED_KEYS:
                return False, f"Key '{key}' is not in allowed keys whitelist", RiskLevel.BLOCKED
            return True, f"Key '{key}' validated", RiskLevel.LOW

        elif t == ActionType.HOTKEY:
            keys = tuple([str(k).lower().strip() for k in p.get("keys", [])])
            if keys not in ALLOWED_HOTKEYS:
                return False, f"Hotkey combination {keys} is not allowed", RiskLevel.BLOCKED
            return True, f"Hotkey {keys} validated", RiskLevel.LOW

        elif t in [ActionType.VOLUME_UP, ActionType.VOLUME_DOWN, ActionType.MUTE, ActionType.UNMUTE]:
            return True, f"Volume action {t.value} validated", RiskLevel.LOW

        elif t == ActionType.LOCK_SCREEN:
            return True, "Lock screen validated", RiskLevel.MEDIUM

        elif t in [ActionType.OPEN_FOLDER, ActionType.OPEN_FILE]:
            filepath = str(p.get("path") or p.get("filename") or "")
            if ".." in filepath or filepath.startswith(("/", "\\")):
                return False, "Path traversal forbidden", RiskLevel.BLOCKED
            return True, f"File action {t.value} validated", RiskLevel.MEDIUM

        elif t in [ActionType.SWITCH_WINDOW, ActionType.MINIMIZE_WINDOW, ActionType.MAXIMIZE_WINDOW]:
            return True, f"Window action {t.value} validated", RiskLevel.LOW

        return False, f"Unsupported action type {t}", RiskLevel.BLOCKED

validator = ActionValidator()
