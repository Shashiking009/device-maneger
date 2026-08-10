import time
import threading
from typing import List, Callable, Dict, Any
from voice.models import VoiceState, VoiceEvent

class VoiceStateMachine:
    """
    Formal State Machine for Spidy Voice Assistant.
    Enforces valid state transitions and broadcasts events to HUD/API subscribers.
    """
    def __init__(self):
        self._state = VoiceState.IDLE
        self._lock = threading.Lock()
        self._listeners: List[Callable[[VoiceEvent], None]] = []

    @property
    def current_state(self) -> VoiceState:
        with self._lock:
            return self._state

    def subscribe(self, callback: Callable[[VoiceEvent], None]):
        with self._lock:
            if callback not in self._listeners:
                self._listeners.append(callback)

    def transition_to(self, new_state: VoiceState, message: str = "", metadata: Dict[str, Any] = None):
        with self._lock:
            old_state = self._state
            self._state = new_state
            event = VoiceEvent(
                event_type=f"TRANSITION_{old_state.value}_TO_{new_state.value}",
                state=new_state,
                timestamp=time.time(),
                message=message or f"State changed to {new_state.value}",
                metadata=metadata or {}
            )
            listeners_copy = list(self._listeners)

        # Notify subscribers without holding lock
        for callback in listeners_copy:
            try:
                callback(event)
            except Exception as e:
                print(f"[VOICE STATE CALLBACK ERROR]: {e}")

voice_state_machine = VoiceStateMachine()
