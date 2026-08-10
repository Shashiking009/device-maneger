import re
from typing import Dict, Any, List, Optional, Tuple
from memory.models import Memory, MemoryCategory, MemorySource
from memory.storage import memory_storage
from memory.secrets import is_secret

class MemoryService:
    """
    High-Level Memory Service Handling Explicit Natural Language & REST Operations.
    """
    def process_memory_command(self, query: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        clean = query.strip().lower()
        clean = re.sub(r"^(hey|hi|ok)\s+spidy[,:]?\s*", "", clean)

        # 1. Clear All Memory ("forget everything", "clear all memory")
        if "forget everything" in clean or "clear all memory" in clean or "delete all memories" in clean:
            return False, "This will delete all long-term memories permanently. Please confirm with 'Yes' to proceed.", {"requires_confirmation": True, "action": "clear_all"}

        # 2. Delete Memory ("forget that...", "forget my...")
        forget_match = re.search(r"\b(forget|delete)\s+(that\s+|my\s+)?([a-z0-9\s]+)", clean)
        if forget_match:
            target = forget_match.group(3).strip()
            key_mapped = self._map_target_to_key(target)
            success = memory_storage.delete_memory(key_mapped)
            if success:
                return True, f"Forgot your '{key_mapped.replace('_', ' ')}'.", {"deleted_key": key_mapped}
            else:
                return False, f"No memory found matching '{target}'.", None

        # 3. Query Memory ("what do you remember", "what is my preferred...")
        if "what do you remember" in clean or "show my memories" in clean or "list memories" in clean:
            summary = self.summarize_memories()
            return True, summary, {"summary": summary}

        # 4. Explicit Memory Save ("remember that...", "my favorite... is...", "I switched to...")
        if "switched to" in clean:
            val = clean.split("switched to")[-1].strip()
            key_mapped = self._map_target_to_key("editor", val)
            mem = Memory(category=MemoryCategory.PREFERENCE, key=key_mapped, value=val, source=MemorySource.USER_CORRECTION, confidence=1.0)
            succ, msg, stored_mem = memory_storage.save_memory(mem)
            return succ, msg, {"memory": stored_mem.model_dump()} if stored_mem else None

        save_match = re.search(r"\b(remember\s+that\s+|remember\s+my\s+|remember\s+|my\s+favorite\s+|i\s+use\s+)?([a-z0-9\s]+?)\s+(is|=|to|as|use|uses|prefer|prefers)\s+([a-z0-9\.\_\-\s]+)", clean)
        if save_match:
            raw_key = (save_match.group(2) or "").strip()
            val = (save_match.group(4) or "").strip()
            key_mapped = self._map_target_to_key(raw_key, val)

            mem = Memory(
                category=MemoryCategory.PREFERENCE if "editor" in key_mapped or "language" in key_mapped else MemoryCategory.LONG_TERM,
                key=key_mapped,
                value=val,
                source=MemorySource.EXPLICIT_USER,
                confidence=1.0,
                importance="MEDIUM"
            )
            succ, msg, stored_mem = memory_storage.save_memory(mem)
            return succ, msg, {"memory": stored_mem.model_dump()} if stored_mem else None

        return False, "Unrecognized memory command format.", None

    def _map_target_to_key(self, target: str, val: str = "") -> str:
        combined = (target + " " + val).lower().strip()
        editors = ["editor", "vscode", "vs code", "code", "pycharm", "sublime", "atom", "vim", "neovim", "emacs", "eclipse", "intellij"]
        if any(e in combined for e in editors):
            return "preferred_editor"
        languages = ["language", "python", "javascript", "typescript", "c++", "java", "rust", "go", "programming"]
        if any(l in combined for l in languages):
            return "preferred_language"
        if "project" in combined:
            return "current_project"
        if "style" in combined or "response" in combined:
            return "response_style"
        return target.replace(" ", "_")

    def summarize_memories(self) -> str:
        memories = memory_storage.list_memories()
        if not memories:
            return "I don't have any saved memories about you yet."

        lines = ["Here is what I remember about you:"]
        for m in memories:
            clean_k = m.key.replace("_", " ").title()
            lines.append(f"- {clean_k}: {m.value}")
        return "\n".join(lines)

memory_service = MemoryService()
