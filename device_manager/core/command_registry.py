import os
from typing import Dict, Any, Callable, Tuple
from core.intent_models import Intent, IntentType, SpidyResponse
from capabilities.capability_registry import capability_registry
from ai.qwen_engine import qwen_engine

class CommandRegistry:
    """
    JARVIS Windows Capability Orchestration Engine.
    Executes intents through safe Windows Capability abstraction layers (AppManager, FileManager, WindowManager, SystemManager, KeyboardController).
    """
    def __init__(self):
        self.cap = capability_registry
        self.handlers: Dict[IntentType, Callable[[Intent], SpidyResponse]] = {
            IntentType.OPEN_APPLICATION: self._handle_open_app,
            IntentType.CLOSE_APPLICATION: self._handle_close_app,
            IntentType.FOCUS_APPLICATION: self._handle_focus_app,
            IntentType.OPEN_FOLDER: self._handle_open_folder,
            IntentType.OPEN_FILE: self._handle_open_file,
            IntentType.SEARCH_FILE: self._handle_search_file,
            IntentType.READ_FILE: self._handle_read_file,
            IntentType.CREATE_FOLDER: self._handle_create_folder,
            IntentType.TYPE_TEXT: self._handle_type_text,
            IntentType.KEY_PRESS: self._handle_key_press,
            IntentType.COPY: self._handle_key_press,
            IntentType.PASTE: self._handle_key_press,
            IntentType.VOLUME_UP: self._handle_volume_up,
            IntentType.VOLUME_DOWN: self._handle_volume_down,
            IntentType.MUTE: self._handle_mute,
            IntentType.UNMUTE: self._handle_unmute,
            IntentType.LOCK_SYSTEM: self._handle_lock_system,
            IntentType.WINDOW_MINIMIZE: self._handle_window_control,
            IntentType.WINDOW_MAXIMIZE: self._handle_window_control,
            IntentType.WINDOW_RESTORE: self._handle_window_control,
            IntentType.WINDOW_CLOSE: self._handle_window_control,
            IntentType.SHOW_DESKTOP: self._handle_window_control,
            IntentType.SYSTEM_STATUS: self._handle_system_status,
            IntentType.PROCESS_STATUS: self._handle_process_status,
            IntentType.GENERAL_AI_QUERY: self._handle_ai_query,
            IntentType.AI_QUESTION: self._handle_ai_query,
            IntentType.HELP: self._handle_help,
        }

    def execute(self, intent: Intent) -> SpidyResponse:
        handler = self.handlers.get(intent.name)
        if not handler:
            return SpidyResponse(
                success=False,
                intent=intent.name,
                message=f"I don't know how to execute capability '{intent.name.value}' yet."
            )
        return handler(intent)

    def _handle_open_app(self, intent: Intent) -> SpidyResponse:
        target = intent.target or intent.parameters.get("app", "")
        succ, msg = self.cap.apps.launch_application(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg, data={"target": target})

    def _handle_close_app(self, intent: Intent) -> SpidyResponse:
        target = intent.target or intent.parameters.get("app", "")
        succ, msg = self.cap.apps.close_application(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg, data={"target": target})

    def _handle_focus_app(self, intent: Intent) -> SpidyResponse:
        target = intent.target or ""
        succ, msg = self.cap.windows.focus_window(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg, data={"target": target})

    def _handle_open_folder(self, intent: Intent) -> SpidyResponse:
        target = intent.target or intent.parameters.get("folder", "downloads")
        succ, msg = self.cap.files.open_folder(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg, data={"folder": target})

    def _handle_open_file(self, intent: Intent) -> SpidyResponse:
        target = intent.target or ""
        succ, msg = self.cap.files.open_file(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg, data={"file": target})

    def _handle_search_file(self, intent: Intent) -> SpidyResponse:
        target = intent.target or ""
        matches = self.cap.files.search_files(target, limit=5)
        if not matches:
            return SpidyResponse(success=False, intent=intent.name, message=f"No files found matching '{target}'.")
        
        names = [m["name"] for m in matches]
        msg = f"I found {len(matches)} files: {', '.join(names)}."
        return SpidyResponse(success=True, intent=intent.name, message=msg, data={"matches": matches})

    def _handle_read_file(self, intent: Intent) -> SpidyResponse:
        target = intent.target or ""
        action = intent.parameters.get("action", "read")
        if action == "summarize":
            succ, msg = self.cap.files.summarize_document(target)
        else:
            succ, msg = self.cap.files.read_text_file(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_create_folder(self, intent: Intent) -> SpidyResponse:
        target = intent.target or "New Folder"
        succ, msg = self.cap.files.create_folder(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_type_text(self, intent: Intent) -> SpidyResponse:
        text = intent.target or intent.parameters.get("text", "")
        succ, msg = self.cap.keyboard.type_text(text)
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_key_press(self, intent: Intent) -> SpidyResponse:
        target = intent.target or "enter"
        succ, msg = self.cap.keyboard.press_key(target)
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_volume_up(self, intent: Intent) -> SpidyResponse:
        succ, msg = self.cap.system.volume_up()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_volume_down(self, intent: Intent) -> SpidyResponse:
        succ, msg = self.cap.system.volume_down()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_mute(self, intent: Intent) -> SpidyResponse:
        succ, msg = self.cap.system.mute()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_unmute(self, intent: Intent) -> SpidyResponse:
        succ, msg = self.cap.system.unmute()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_lock_system(self, intent: Intent) -> SpidyResponse:
        succ, msg = self.cap.system.lock_laptop()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_window_control(self, intent: Intent) -> SpidyResponse:
        if intent.name == IntentType.WINDOW_MINIMIZE:
            succ, msg = self.cap.windows.minimize_active_window()
        elif intent.name == IntentType.WINDOW_MAXIMIZE:
            succ, msg = self.cap.windows.maximize_active_window()
        elif intent.name == IntentType.WINDOW_RESTORE:
            succ, msg = self.cap.windows.restore_active_window()
        elif intent.name == IntentType.WINDOW_CLOSE:
            succ, msg = self.cap.windows.close_active_window()
        elif intent.name == IntentType.SHOW_DESKTOP:
            succ, msg = self.cap.windows.show_desktop()
        else:
            succ, msg = False, "Unknown window action."
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_system_status(self, intent: Intent) -> SpidyResponse:
        if intent.target == "self_diagnostics":
            succ, msg = self.cap.system.self_diagnostics()
        else:
            succ, msg = self.cap.system.system_status()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_process_status(self, intent: Intent) -> SpidyResponse:
        target = intent.target or intent.parameters.get("app", "")
        if target:
            succ, msg = self.cap.system.is_app_running(target)
        else:
            succ, msg = self.cap.system.process_status()
        return SpidyResponse(success=succ, intent=intent.name, message=msg)

    def _handle_ai_query(self, intent: Intent) -> SpidyResponse:
        query = intent.target or intent.parameters.get("raw_cmd", "")
        prompt = f"Answer the user's question concisely in 2 sentences:\nUser Question: {query}"
        reply, tps = qwen_engine.generate_ai_response(prompt)
        ans = reply.strip() if reply else "I couldn't process that question right now."
        return SpidyResponse(success=True, intent=intent.name, message=ans)

    def _handle_help(self, intent: Intent) -> SpidyResponse:
        msg = "I can open applications, search files, control volume and windows, type text, answer questions, remember preferences, and monitor your system."
        return SpidyResponse(success=True, intent=intent.name, message=msg)

command_registry = CommandRegistry()
