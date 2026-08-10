from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class IntentType(str, Enum):
    OPEN_APPLICATION = "OPEN_APPLICATION"
    CLOSE_APPLICATION = "CLOSE_APPLICATION"
    TYPE_TEXT = "TYPE_TEXT"
    KEY_PRESS = "KEY_PRESS"
    COPY = "COPY"
    PASTE = "PASTE"
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    MUTE = "MUTE"
    UNMUTE = "UNMUTE"
    LOCK_SYSTEM = "LOCK_SYSTEM"
    OPEN_FOLDER = "OPEN_FOLDER"
    OPEN_FILE = "OPEN_FILE"
    SYSTEM_STATUS = "SYSTEM_STATUS"
    AI_QUESTION = "AI_QUESTION"
    RAG_QUERY = "RAG_QUERY"
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
    requires_confirmation: bool = False
    sources: Optional[List[Dict[str, Any]]] = None
    tokens_per_sec: Optional[float] = None
