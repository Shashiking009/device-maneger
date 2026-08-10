from core.intent_models import Intent, IntentType, RiskLevel

class PermissionManager:
    """
    Manages risk assessment and permission validation for Spidy intents.
    Prevents unauthorized or dangerous system operations.
    """
    def __init__(self):
        self.risk_mapping = {
            IntentType.OPEN_APPLICATION: RiskLevel.LOW,
            IntentType.CLOSE_APPLICATION: RiskLevel.LOW,
            IntentType.TYPE_TEXT: RiskLevel.LOW,
            IntentType.KEY_PRESS: RiskLevel.LOW,
            IntentType.COPY: RiskLevel.LOW,
            IntentType.PASTE: RiskLevel.LOW,
            IntentType.VOLUME_UP: RiskLevel.LOW,
            IntentType.VOLUME_DOWN: RiskLevel.LOW,
            IntentType.MUTE: RiskLevel.LOW,
            IntentType.UNMUTE: RiskLevel.LOW,
            IntentType.OPEN_FOLDER: RiskLevel.LOW,
            IntentType.OPEN_FILE: RiskLevel.LOW,
            IntentType.SYSTEM_STATUS: RiskLevel.LOW,
            IntentType.AI_QUESTION: RiskLevel.LOW,
            IntentType.RAG_QUERY: RiskLevel.LOW,
            IntentType.LOCK_SYSTEM: RiskLevel.MEDIUM,
            IntentType.UNKNOWN: RiskLevel.LOW,
        }

    def assess_risk(self, intent: Intent) -> RiskLevel:
        level = self.risk_mapping.get(intent.name, RiskLevel.LOW)
        intent.risk_level = level
        if level in [RiskLevel.MEDIUM, RiskLevel.HIGH] and intent.parameters.get("ask_confirmation", False):
            intent.requires_confirmation = True
        return level

    def is_permitted(self, intent: Intent) -> bool:
        # High risk actions (e.g. raw shell execution or file deletion) are strictly prohibited
        if intent.risk_level == RiskLevel.HIGH and not intent.requires_confirmation:
            return False
        return True
