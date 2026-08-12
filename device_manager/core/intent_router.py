import re
from typing import Tuple, Dict, Any, Optional
from core.intent_models import Intent, IntentType, RiskLevel
from capabilities.app_manager import app_manager
from capabilities.file_manager import file_manager
from ai.qwen_engine import qwen_engine

class IntentRouter:
    """
    JARVIS-Style Intent Classification Router:
    1. Fast Deterministic Regex & Keyword Matching (0ms latency)
    2. Dynamic Capability Matching (ApplicationManager, FileManager, WindowManager)
    3. Qwen3 SLM Fallback Classifier for ambiguous natural language
    """
    def classify_deterministic(self, clean_input: str) -> Optional[Intent]:
        cmd = clean_input.lower().strip()
        if not cmd:
            return None

        # 1. Self Diagnostics & Help
        if any(w in cmd for w in ["are you working", "are you operational", "system check", "self test"]):
            return Intent(name=IntentType.SYSTEM_STATUS, target="self_diagnostics", confidence=1.0)
        if cmd in ["help", "what can you do", "commands", "what commands"]:
            return Intent(name=IntentType.HELP, confidence=1.0)
        if cmd in ["stop", "quiet", "stop talking", "hush", "shut up"]:
            return Intent(name=IntentType.STOP_SPEAKING, confidence=1.0)

        # 2. Volume & Audio Controls
        if any(v in cmd for v in ["volume up", "increase volume", "raise volume", "turn up volume", "louder"]):
            return Intent(name=IntentType.VOLUME_UP, confidence=1.0)
        if any(v in cmd for v in ["volume down", "decrease volume", "lower volume", "turn down volume", "quiet"]):
            return Intent(name=IntentType.VOLUME_DOWN, confidence=1.0)
        if "unmute" in cmd:
            return Intent(name=IntentType.UNMUTE, confidence=1.0)
        if "mute" in cmd:
            return Intent(name=IntentType.MUTE, confidence=1.0)

        # 3. Lock & Window Controls
        if any(l in cmd for l in ["lock laptop", "lock computer", "lock screen", "lock my laptop"]) or cmd == "lock":
            return Intent(name=IntentType.LOCK_SYSTEM, confidence=1.0, risk_level=RiskLevel.MEDIUM)
        if any(w in cmd for w in ["show desktop", "minimize all", "hide all windows"]):
            return Intent(name=IntentType.SHOW_DESKTOP, confidence=1.0)
        if "minimize" in cmd:
            return Intent(name=IntentType.WINDOW_MINIMIZE, confidence=1.0)
        if "maximize" in cmd:
            return Intent(name=IntentType.WINDOW_MAXIMIZE, confidence=1.0)
        if "restore window" in cmd:
            return Intent(name=IntentType.WINDOW_RESTORE, confidence=1.0)
        if "close window" in cmd or "close this window" in cmd:
            return Intent(name=IntentType.WINDOW_CLOSE, confidence=1.0)

        # 4. System Telemetry & Process Inspection
        if any(s in cmd for s in ["system status", "how is my laptop", "cpu usage", "ram usage", "battery status"]):
            return Intent(name=IntentType.SYSTEM_STATUS, confidence=1.0)
        
        is_running_match = re.search(r'^(?:is|check if)\s+(.+?)\s+(?:running|open|active)\??$', cmd)
        if is_running_match:
            return Intent(name=IntentType.PROCESS_STATUS, target=is_running_match.group(1).strip(), confidence=1.0)

        if any(p in cmd for p in ["processes", "process status", "how many processes", "running applications"]):
            return Intent(name=IntentType.PROCESS_STATUS, confidence=1.0)

        # 5. Local Memory Commands
        if any(m in cmd for m in ["forget everything", "clear all memory", "delete all memories"]):
            return Intent(name=IntentType.MEMORY_CLEAR, confidence=1.0, requires_confirmation=True, risk_level=RiskLevel.HIGH)
        if "forget" in cmd or "delete memory" in cmd:
            return Intent(name=IntentType.MEMORY_DELETE, confidence=1.0)
        if any(m in cmd for m in ["what do you remember", "show my memories", "list memories"]):
            return Intent(name=IntentType.MEMORY_QUERY, confidence=1.0)
        if "remember" in cmd or "my favorite" in cmd or "i use" in cmd or "switched to" in cmd:
            return Intent(name=IntentType.MEMORY_SAVE, confidence=1.0)

        # 6. RAG Grounded Queries
        if any(p in cmd for p in ["knowledge base", "my project plan", "my documents", "my files", "in my document", "document says"]):
            return Intent(name=IntentType.RAG_QUERY, confidence=1.0)

        # 7. Text Typing & Automation Controls
        if "select all" in cmd:
            return Intent(name=IntentType.KEY_PRESS, target="ctrl+a", confidence=1.0)
        if "copy" in cmd and "file" not in cmd and "folder" not in cmd:
            return Intent(name=IntentType.COPY, confidence=1.0)
        if "paste" in cmd:
            return Intent(name=IntentType.PASTE, confidence=1.0)
        
        type_match = re.search(r'^(?:type|write|say)\s+(.+)', cmd)
        if type_match:
            return Intent(name=IntentType.TYPE_TEXT, target=type_match.group(1).strip(), confidence=1.0)

        if "press enter" in cmd or "hit enter" in cmd:
            return Intent(name=IntentType.KEY_PRESS, target="enter", confidence=1.0)
        if "press space" in cmd or "hit space" in cmd:
            return Intent(name=IntentType.KEY_PRESS, target="space", confidence=1.0)

        # 8. File Search & Document Summarization
        create_fold_match = re.search(r'^(?:create|make|new)\s+folder\s+(.+)', cmd)
        if create_fold_match:
            return Intent(name=IntentType.CREATE_FOLDER, target=create_fold_match.group(1).strip(), confidence=1.0)

        sum_match = re.search(r'^(?:summarize|summary of|read)\s+(?:file|document|doc)?\s*(.+)', cmd)
        if sum_match and any(w in cmd for w in ["summarize", "summary"]):
            return Intent(name=IntentType.READ_FILE, target=sum_match.group(1).strip(), parameters={"action": "summarize"}, confidence=1.0)

        find_match = re.search(r'^(?:find|search|look for)\s+(?:file|files|folder|my)?\s*(.+)', cmd)
        if find_match and "app" not in cmd and "application" not in cmd:
            target_query = find_match.group(1).strip()
            return Intent(name=IntentType.SEARCH_FILE, target=target_query, confidence=1.0)

        # 9. Window Focus / Switching
        switch_match = re.search(r'^(?:switch to|focus|bring up)\s+(.+)', cmd)
        if switch_match:
            return Intent(name=IntentType.FOCUS_APPLICATION, target=switch_match.group(1).strip(), confidence=1.0)

        # 10. Application Closing
        close_match = re.search(r'^(?:close|quit|exit|stop|kill|terminate)\s+(.+)', cmd)
        if close_match and "window" not in cmd and "memory" not in cmd:
            return Intent(name=IntentType.CLOSE_APPLICATION, target=close_match.group(1).strip(), confidence=1.0)

        # 11. Folder Opening
        folder_match = re.search(r'^(?:open|show)\s+(?:my\s+)?([a-z0-9\s]+?)\s*(?:folder|directory)?$', cmd)
        if folder_match:
            potential_folder = folder_match.group(1).strip()
            if file_manager.resolve_folder_path(potential_folder):
                return Intent(name=IntentType.OPEN_FOLDER, target=potential_folder, confidence=1.0)

        # 12. Dynamic Application Opening
        open_app_match = re.search(r'^(?:open|launch|start|run)\s+(.+)', cmd)
        if open_app_match:
            target_app_query = open_app_match.group(1).strip()
            # Check if target matches an app in app_manager
            found_app = app_manager.find_application(target_app_query)
            if found_app:
                return Intent(name=IntentType.OPEN_APPLICATION, target=found_app.name, confidence=1.0)

        # 13. General AI Questions ("what is...", "explain...", "how to...")
        if any(cmd.startswith(prefix) for prefix in ["what is", "what are", "who is", "explain", "how to", "tell me about"]):
            return Intent(name=IntentType.GENERAL_AI_QUERY, target=clean_input, confidence=0.9)

        return None

    def route(self, user_input: str) -> Intent:
        clean_input = re.sub(r'^(hey|hi|hello|ok|okay)?\s*(spidy|spidey|spider)\s*', '', user_input.lower().strip()).strip()
        if not clean_input:
            clean_input = user_input.lower().strip()

        # Step 1: Fast Deterministic Match
        det_intent = self.classify_deterministic(clean_input)
        if det_intent:
            return det_intent

        # Step 2: Dynamic App Discovery Match
        app = app_manager.find_application(clean_input)
        if app:
            return Intent(name=IntentType.OPEN_APPLICATION, target=app.name, confidence=0.9)

        # Step 3: Fallback to Qwen3 SLM Classifier
        qwen_json = qwen_engine.classify_intent_with_qwen(clean_input)
        if qwen_json and isinstance(qwen_json, dict):
            name_str = qwen_json.get("name", "GENERAL_AI_QUERY").upper()
            target_str = qwen_json.get("target")
            confidence = float(qwen_json.get("confidence", 0.8))

            try:
                intent_enum = IntentType(name_str)
                return Intent(
                    name=intent_enum,
                    target=target_str,
                    parameters=qwen_json.get("parameters", {}),
                    confidence=confidence
                )
            except Exception:
                pass

        return Intent(name=IntentType.GENERAL_AI_QUERY, target=user_input, confidence=0.7)
