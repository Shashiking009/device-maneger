from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class IntentType(str, Enum):
    # Application Controls
    OPEN_APPLICATION = "OPEN_APPLICATION"
    CLOSE_APPLICATION = "CLOSE_APPLICATION"
    FOCUS_APPLICATION = "FOCUS_APPLICATION"

    # File System Controls
    OPEN_FOLDER = "OPEN_FOLDER"
    OPEN_FILE = "OPEN_FILE"
    SEARCH_FILE = "SEARCH_FILE"
    LIST_FILES = "LIST_FILES"
    CREATE_FOLDER = "CREATE_FOLDER"
    CREATE_FILE = "CREATE_FILE"
    READ_FILE = "READ_FILE"

    # Input & Automation
    TYPE_TEXT = "TYPE_TEXT"
    KEY_PRESS = "KEY_PRESS"
    COPY = "COPY"
    PASTE = "PASTE"

    # Audio & System Controls
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    MUTE = "MUTE"
    UNMUTE = "UNMUTE"
    LOCK_SYSTEM = "LOCK_SYSTEM"
    SLEEP_SYSTEM = "SLEEP_SYSTEM"

    # Window Controls
    WINDOW_MINIMIZE = "WINDOW_MINIMIZE"
    WINDOW_MAXIMIZE = "WINDOW_MAXIMIZE"
    WINDOW_RESTORE = "WINDOW_RESTORE"
    WINDOW_CLOSE = "WINDOW_CLOSE"
    SHOW_DESKTOP = "SHOW_DESKTOP"

    # Telemetry & Status
    SYSTEM_STATUS = "SYSTEM_STATUS"
    PROCESS_STATUS = "PROCESS_STATUS"

    # Local Memory Engine
    MEMORY_SAVE = "MEMORY_SAVE"
    MEMORY_QUERY = "MEMORY_QUERY"
    MEMORY_DELETE = "MEMORY_DELETE"
    MEMORY_CLEAR = "MEMORY_CLEAR"

    # AI & RAG Intelligence
    RAG_QUERY = "RAG_QUERY"
    GENERAL_AI_QUERY = "GENERAL_AI_QUERY"
    AI_QUESTION = "AI_QUESTION"

    # Voice Assistant Utility
    HELP = "HELP"
    STOP_SPEAKING = "STOP_SPEAKING"
    UNKNOWN = "UNKNOWN"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Intent(BaseModel):
    name: IntentType
    target: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    requires_confirmation: bool = False
    risk_level: RiskLevel = RiskLevel.LOW

class SpidyResponse(BaseModel):
    success: bool
    intent: IntentType
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)
