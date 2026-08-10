import time
import json
import asyncio
from typing import Dict, Any, List, Set, Optional
from pydantic import BaseModel, Field

class SpidyEvent(BaseModel):
    event_type: str
    state: str = "IDLE"
    timestamp: float = Field(default_factory=time.time)
    message: str = ""
    data: Dict[str, Any] = Field(default_factory=dict)

class SpidyEventBus:
    """
    Centralized Real-Time Event Bus for Spidy AI.
    Publishes events to connected WebSocket clients (HUD, Dashboard, API monitors).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpidyEventBus, cls).__new__(cls)
            cls._instance.connections: Set[Any] = set()
            cls._instance.event_history: List[Dict[str, Any]] = []
        return cls._instance

    def register_ws(self, ws: Any):
        self.connections.add(ws)

    def unregister_ws(self, ws: Any):
        self.connections.discard(ws)

    def publish(self, event: SpidyEvent):
        event_dict = event.model_dump()
        
        # Maintain short recent history (max 50 events)
        self.event_history.append(event_dict)
        if len(self.event_history) > 50:
            self.event_history.pop(0)

        # Broadcast asynchronously to all active WebSocket connections
        dead_connections = set()
        for ws in list(self.connections):
            try:
                # If running inside asyncio loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(ws.send_json(event_dict))
                else:
                    asyncio.run(ws.send_json(event_dict))
            except Exception:
                dead_connections.add(ws)

        for dead in dead_connections:
            self.connections.discard(dead)

event_bus = SpidyEventBus()
