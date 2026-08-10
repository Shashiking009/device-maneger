import time
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class VoiceState(str, Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    EXECUTING = "EXECUTING"
    SPEAKING = "SPEAKING"
    ERROR = "ERROR"
    STOPPED = "STOPPED"

class VoiceEvent(BaseModel):
    event_type: str
    state: VoiceState
    timestamp: float = Field(default_factory=time.time)
    message: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
