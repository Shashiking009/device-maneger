import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class MemoryCategory(str, Enum):
    SHORT_TERM = "SHORT_TERM"
    SESSION = "SESSION"
    LONG_TERM = "LONG_TERM"
    PREFERENCE = "PREFERENCE"

class MemorySource(str, Enum):
    EXPLICIT_USER = "EXPLICIT_USER"
    USER_CORRECTION = "USER_CORRECTION"
    SYSTEM_DERIVED = "SYSTEM_DERIVED"
    SESSION_SUMMARY = "SESSION_SUMMARY"

class Memory(BaseModel):
    id: str = Field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:8]}")
    category: MemoryCategory
    key: str
    value: str
    source: MemorySource = MemorySource.EXPLICIT_USER
    confidence: float = 1.0
    importance: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    scope: str = "PERMANENT"    # PERMANENT, SESSION, TEMPORARY
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    last_used_at: float = Field(default_factory=time.time)
    expires_at: Optional[float] = None

class ConversationContext(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    summary: str = ""
    relevant_memories: List[Memory] = Field(default_factory=list)
    relevant_rag: List[str] = Field(default_factory=list)
