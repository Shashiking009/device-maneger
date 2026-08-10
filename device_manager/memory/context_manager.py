from typing import List, Dict, Any, Optional
from memory.models import Memory, ConversationContext, MemoryCategory
from memory.storage import memory_storage
from database import get_session_messages

class ContextManager:
    """
    Spidy AI Context Assembly Engine.
    Filters relevant memories, manages session boundaries, and resolves pronoun references.
    """
    def build_context(self, user_input: str, session_id: Optional[str] = None) -> ConversationContext:
        clean_input = user_input.lower().strip()

        # 1. Fetch relevant memories (filtered by key/category relevance)
        all_memories = memory_storage.list_memories()
        relevant: List[Memory] = []

        for mem in all_memories:
            # Check key or value match in input
            if mem.key.lower() in clean_input or mem.value.lower() in clean_input or "remember" in clean_input or "about me" in clean_input:
                relevant.append(mem)
            elif "editor" in clean_input and mem.key == "preferred_editor":
                relevant.append(mem)
            elif "language" in clean_input and mem.key == "preferred_language":
                relevant.append(mem)

        # 2. Fetch recent session messages
        recent_messages: List[Dict[str, Any]] = []
        summary = ""
        if session_id:
            try:
                msgs = get_session_messages(session_id)
                # Cap to recent 10 turns
                recent_messages = msgs[-10:] if len(msgs) > 10 else msgs
            except Exception as e:
                print(f"[CONTEXT MANAGER WARNING]: Session msgs error: {e}")

        return ConversationContext(
            session_id=session_id or "default",
            messages=recent_messages,
            summary=summary,
            relevant_memories=relevant
        )

    def resolve_reference(self, user_input: str, session_id: Optional[str] = None) -> str:
        """
        Resolves pronouns ('it', 'my editor', 'my language') using memory or last turn.
        """
        clean = user_input.lower().strip()
        
        # Check preference references
        if "my editor" in clean or "open my editor" in clean:
            mem = memory_storage.get_memory("preferred_editor")
            if mem:
                return user_input.replace("my editor", mem.value)

        if "my language" in clean or "my favorite language" in clean:
            mem = memory_storage.get_memory("preferred_language")
            if mem:
                return user_input.replace("my favorite language", mem.value).replace("my language", mem.value)

        # Check last turn pronoun "it" or "that"
        if ("what is" in clean or "who created" in clean or "tell me about" in clean) and (" it" in clean or " that" in clean):
            if session_id:
                try:
                    msgs = get_session_messages(session_id)
                    if msgs:
                        last_msg = msgs[-1].get("content", "")
                        # Simple topic extraction from last message
                        topic = last_msg.replace("What is", "").replace("who created", "").strip("? ")
                        if topic and len(topic) < 40:
                            return user_input.replace(" it", f" {topic}").replace(" that", f" {topic}")
                except Exception:
                    pass

        return user_input

context_manager = ContextManager()
