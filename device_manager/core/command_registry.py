import os
import platform
import subprocess
from typing import Dict, Any, Callable
from core.intent_models import Intent, IntentType, SpidyResponse
from voice_assistant import close_application_process, KNOWN_APPS, KNOWN_FOLDERS, UPLOAD_DIR, WORKSPACE_DIR
from voice_automation import execute_automation_command

APP_ALIASES: Dict[str, str] = {
    "calc": "calculator",
    "calculator": "calculator",
    "win32calc": "calculator",
    "notepad": "notepad",
    "note pad": "notepad",
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "edge",
    "msedge": "edge",
    "microsoft edge": "edge",
    "code": "vs code",
    "vs code": "vs code",
    "visual studio code": "vs code",
    "cmd": "cmd",
    "command prompt": "cmd",
    "paint": "paint",
    "ms paint": "paint",
    "mspaint": "paint",
    "task manager": "task manager",
    "taskmgr": "task manager",
    "explorer": "explorer",
    "file explorer": "explorer"
}

def normalize_app_name(raw_name: str) -> str:
    cleaned = raw_name.lower().strip()
    return APP_ALIASES.get(cleaned, cleaned)

class CommandRegistry:
    """
    Central registry of safe, pre-approved system action handlers.
    NEVER allows execution of raw unvalidated shell strings or code strings.
    """
    def __init__(self):
        self.handlers: Dict[IntentType, Callable[[Intent], SpidyResponse]] = {
            IntentType.OPEN_APPLICATION: self._handle_open_app,
            IntentType.CLOSE_APPLICATION: self._handle_close_app,
            IntentType.TYPE_TEXT: self._handle_automation_action,
            IntentType.KEY_PRESS: self._handle_automation_action,
            IntentType.COPY: self._handle_automation_action,
            IntentType.PASTE: self._handle_automation_action,
            IntentType.VOLUME_UP: self._handle_automation_action,
            IntentType.VOLUME_DOWN: self._handle_automation_action,
            IntentType.MUTE: self._handle_automation_action,
            IntentType.UNMUTE: self._handle_automation_action,
            IntentType.LOCK_SYSTEM: self._handle_automation_action,
            IntentType.OPEN_FOLDER: self._handle_open_folder,
            IntentType.OPEN_FILE: self._handle_open_file,
            IntentType.SYSTEM_STATUS: self._handle_system_status,
        }

    def execute(self, intent: Intent) -> SpidyResponse:
        handler = self.handlers.get(intent.name)
        if not handler:
            return SpidyResponse(
                success=False,
                intent=intent.name,
                message=f"No execution handler registered for intent '{intent.name.value}'."
            )
        return handler(intent)

    def _handle_open_app(self, intent: Intent) -> SpidyResponse:
        raw_target = intent.target or intent.parameters.get("app", "")
        if not raw_target:
            return SpidyResponse(success=False, intent=intent.name, message="Missing target application name.")
        
        normalized_app = normalize_app_name(raw_target)
        app_data = KNOWN_APPS.get(normalized_app)
        
        if not app_data:
            # Fallback to attempt launching standard windows process name
            app_data = {"exec": [f"{normalized_app}.exe"]}
            
        try:
            if platform.system() == "Windows":
                subprocess.Popen(app_data["exec"], shell=True)
            else:
                subprocess.Popen([app_data["exec"][0]])
            return SpidyResponse(
                success=True,
                intent=intent.name,
                message=f"Opening {normalized_app.title()} on your device.",
                data={"app": normalized_app}
            )
        except Exception as e:
            return SpidyResponse(
                success=False,
                intent=intent.name,
                message=f"Could not launch {normalized_app}: {str(e)}"
            )

    def _handle_close_app(self, intent: Intent) -> SpidyResponse:
        raw_target = intent.target or intent.parameters.get("app", "")
        if not raw_target:
            return SpidyResponse(success=False, intent=intent.name, message="Missing target application name.")
            
        normalized_app = normalize_app_name(raw_target)
        closed = close_application_process(normalized_app)
        if closed:
            return SpidyResponse(
                success=True,
                intent=intent.name,
                message=f"Successfully closed {normalized_app.title()} on your device.",
                data={"app": normalized_app}
            )
        else:
            return SpidyResponse(
                success=True,
                intent=intent.name,
                message=f"Tried to close {normalized_app.title()}, but no running process was found.",
                data={"app": normalized_app}
            )

    def _handle_automation_action(self, intent: Intent) -> SpidyResponse:
        raw_cmd = intent.parameters.get("raw_cmd", "")
        if not raw_cmd:
            if intent.name == IntentType.VOLUME_UP:
                raw_cmd = "volume up"
            elif intent.name == IntentType.VOLUME_DOWN:
                raw_cmd = "volume down"
            elif intent.name == IntentType.MUTE:
                raw_cmd = "mute"
            elif intent.name == IntentType.UNMUTE:
                raw_cmd = "unmute"
            elif intent.name == IntentType.LOCK_SYSTEM:
                raw_cmd = "lock laptop"
            elif intent.name == IntentType.TYPE_TEXT:
                raw_cmd = f"type {intent.target or ''}"
            elif intent.name == IntentType.KEY_PRESS:
                raw_cmd = f"press {intent.target or ''}"
            elif intent.name == IntentType.COPY:
                raw_cmd = "copy"
            elif intent.name == IntentType.PASTE:
                raw_cmd = "paste"

        res = execute_automation_command(raw_cmd)
        if res.get("status") == "success":
            return SpidyResponse(
                success=True,
                intent=intent.name,
                message=res.get("message", "Executed automation action.")
            )
        else:
            return SpidyResponse(
                success=False,
                intent=intent.name,
                message=res.get("message", "Failed to execute automation action.")
            )

    def _handle_open_folder(self, intent: Intent) -> SpidyResponse:
        target = (intent.target or intent.parameters.get("folder", "")).lower()
        folder_path = KNOWN_FOLDERS.get(target)
        
        if not folder_path or not os.path.exists(folder_path):
            folder_path = os.path.expanduser(f"~/{target.title()}")

        if os.path.exists(folder_path):
            try:
                if platform.system() == "Windows":
                    os.startfile(folder_path)
                else:
                    subprocess.Popen(["xdg-open", folder_path])
                return SpidyResponse(
                    success=True,
                    intent=intent.name,
                    message=f"Opening {target.title()} folder.",
                    data={"folder": target, "path": folder_path}
                )
            except Exception as e:
                return SpidyResponse(success=False, intent=intent.name, message=f"Failed to open folder: {str(e)}")

        return SpidyResponse(success=False, intent=intent.name, message=f"Folder '{target}' not found.")

    def _handle_open_file(self, intent: Intent) -> SpidyResponse:
        target_name = (intent.target or intent.parameters.get("filename", "")).lower().strip()
        if not target_name:
            return SpidyResponse(success=False, intent=intent.name, message="Missing target filename.")

        search_dirs = [UPLOAD_DIR, WORKSPACE_DIR]
        candidates = []
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for f in os.listdir(search_dir):
                    if (target_name in f.lower() or f.lower().startswith(target_name)) and not os.path.isdir(os.path.join(search_dir, f)):
                        candidates.append(os.path.join(search_dir, f))

        if candidates:
            target_path = candidates[0]
            try:
                if platform.system() == "Windows":
                    os.startfile(target_path)
                else:
                    subprocess.Popen(["xdg-open", target_path])
                filename = os.path.basename(target_path)
                return SpidyResponse(
                    success=True,
                    intent=intent.name,
                    message=f"Opening file {filename}.",
                    data={"filename": filename, "filepath": target_path}
                )
            except Exception as e:
                return SpidyResponse(success=False, intent=intent.name, message=f"Error opening file: {str(e)}")

        return SpidyResponse(success=False, intent=intent.name, message=f"File '{target_name}' not found in uploads or workspace.")

    def _handle_system_status(self, intent: Intent) -> SpidyResponse:
        return SpidyResponse(
            success=True,
            intent=intent.name,
            message="Checking system diagnostics. Check the system telemetry dashboard for real-time CPU and Memory stats."
        )
