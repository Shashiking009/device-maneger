import time
import re
from typing import Dict, Any, List, Optional
from system.window_context import window_context

class ConversationContext:
    """
    JARVIS Conversational Context & Reference Resolution Engine.
    Maintains a rolling bounded conversation history, tracks active subjects & session objects,
    and resolves ambiguous pronoun references ("it", "that", "the app", "who created it?").
    """
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history: List[Dict[str, Any]] = []
        
        # Session State Tracking
        self.last_application: Optional[str] = None
        self.current_application: Optional[str] = None
        self.last_file: Optional[str] = None
        self.last_folder: Optional[str] = None
        self.last_url: Optional[str] = None
        self.last_search: Optional[str] = None
        self.last_ai_topic: Optional[str] = None
        self.last_action: Optional[str] = None
        self.last_action_result: Optional[str] = None

    def add_turn(self, role: str, text: str, intent: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        turn = {
            "role": role,
            "text": text,
            "intent": intent,
            "metadata": metadata or {},
            "timestamp": time.time()
        }
        self.history.append(turn)
        if len(self.history) > self.max_turns:
            self.history.pop(0)

        # Explicit Turn Metadata update (takes priority over background active window)
        if metadata:
            if "app_name" in metadata and metadata["app_name"]:
                self.last_application = metadata["app_name"]
            if "folder_name" in metadata and metadata["folder_name"]:
                self.last_folder = metadata["folder_name"]
            if "file_name" in metadata and metadata["file_name"]:
                self.last_file = metadata["file_name"]
            if "ai_topic" in metadata and metadata["ai_topic"]:
                self.last_ai_topic = metadata["ai_topic"]
            if "search_query" in metadata and metadata["search_query"]:
                self.last_search = metadata["search_query"]
            if "action" in metadata and metadata["action"]:
                self.last_action = metadata["action"]

    def update_window_state(self):
        info = window_context.get_active_window_info()
        self.current_application = info.get("app_alias")

    def resolve_references(self, text: str) -> str:
        if not text:
            return ""

        lower = text.lower().strip()
        resolved = text

        # Update active focused window state
        self.update_window_state()

        # 1. Resolve Application References ("it", "that app", "the app", "the application")
        if re.search(r'\b(close|minimize|maximize|restore|focus|quit|exit)\s+(it|that|this|the app|the application)\b', lower):
            target_app = self.last_application or self.current_application
            if target_app:
                resolved = re.sub(
                    r'\b(close|minimize|maximize|restore|focus|quit|exit)\s+(it|that|this|the app|the application)\b',
                    rf'\1 {target_app}',
                    resolved,
                    flags=re.IGNORECASE
                )

        # 2. Resolve Folder References ("that folder", "the folder", "it", "there")
        if re.search(r'\b(open|show|create)\s+(that folder|the folder|there)\b', lower):
            if self.last_folder:
                resolved = re.sub(
                    r'\b(open|show|create)\s+(that folder|the folder|there)\b',
                    rf'\1 {self.last_folder}',
                    resolved,
                    flags=re.IGNORECASE
                )

        # 3. Resolve File References ("that file", "the file", "it")
        if re.search(r'\b(open|read|summarize|delete)\s+(that file|the file)\b', lower):
            if self.last_file:
                resolved = re.sub(
                    r'\b(open|read|summarize|delete)\s+(that file|the file)\b',
                    rf'\1 {self.last_file}',
                    resolved,
                    flags=re.IGNORECASE
                )

        # 4. Resolve Follow-up AI Subject Pronouns ("who created it?", "is it good for AI?")
        if self.last_ai_topic:
            if re.search(r'\b(who|what|why|how|when|is|can|does|tell me about)\b.*?\b(it|that|this)\b', lower):
                if not re.search(r'\b(open|close|launch|start|run|minimize|maximize)\b', lower):
                    resolved = re.sub(r'\b(it|that|this)\b', self.last_ai_topic, resolved, flags=re.IGNORECASE)

        return resolved

    def extract_ai_topic(self, user_input: str) -> Optional[str]:
        lower = user_input.lower().strip()
        clean = re.sub(r'^(what is|who is|tell me about|explain|how does|what are|who created|is)\s+', '', lower, flags=re.IGNORECASE)
        clean = clean.rstrip("?!. ")
        if clean and len(clean) > 2:
            return clean.capitalize()
        return None

    def get_bounded_context_prompt(self, max_messages: int = 4) -> str:
        recent = self.history[-max_messages:]
        if not recent:
            return ""
        lines = []
        for turn in recent:
            lines.append(f"{turn['role'].upper()}: {turn['text']}")
        return "\n".join(lines)

conversation_context = ConversationContext()
