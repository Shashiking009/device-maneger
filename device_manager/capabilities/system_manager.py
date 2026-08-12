import os
import psutil
import requests
from typing import Dict, Any, Tuple
from voice_automation import execute_automation_command
from telemetry import get_system_telemetry
from config import OLLAMA_HOST, OLLAMA_MODEL

class SystemManager:
    """
    Windows System Controls & Diagnostic Telemetry Engine.
    Handles volume, lock/sleep, process inspection, and JARVIS self-diagnostics.
    """
    def volume_up(self) -> Tuple[bool, str]:
        res = execute_automation_command("volume up")
        succ = isinstance(res, dict) and res.get("status") == "success"
        return succ, "Volume increased." if succ else "Failed to adjust volume."

    def volume_down(self) -> Tuple[bool, str]:
        res = execute_automation_command("volume down")
        succ = isinstance(res, dict) and res.get("status") == "success"
        return succ, "Volume decreased." if succ else "Failed to adjust volume."

    def mute(self) -> Tuple[bool, str]:
        res = execute_automation_command("mute")
        succ = isinstance(res, dict) and res.get("status") == "success"
        return succ, "Audio muted." if succ else "Failed to mute audio."

    def unmute(self) -> Tuple[bool, str]:
        res = execute_automation_command("unmute")
        succ = isinstance(res, dict) and res.get("status") == "success"
        return succ, "Audio unmuted." if succ else "Failed to unmute audio."

    def lock_laptop(self) -> Tuple[bool, str]:
        res = execute_automation_command("lock")
        succ = isinstance(res, dict) and res.get("status") == "success"
        return succ, "Locking laptop." if succ else "Failed to lock laptop."

    def system_status(self) -> Tuple[bool, str]:
        t = get_system_telemetry()
        msg = f"CPU usage is {round(t.cpu_percent)} percent, RAM usage is {round(t.memory_percent)} percent across {t.processes} active processes."
        return True, msg

    def process_status(self) -> Tuple[bool, str]:
        count = len(psutil.pids())
        return True, f"There are currently {count} active system processes running."

    def is_app_running(self, app_name: str) -> Tuple[bool, str]:
        clean = app_name.lower().strip()
        for proc in psutil.process_iter(['name']):
            try:
                pname = proc.info['name'].lower()
                if clean in pname:
                    return True, f"Yes, {app_name.title()} is currently running."
            except Exception:
                pass
        return True, f"No, {app_name.title()} is not currently running."

    def self_diagnostics(self) -> Tuple[bool, str]:
        from database import check_db_integrity
        from voice.audio_manager import audio_manager
        from rag.rag_engine import rag_service

        db_ok = check_db_integrity()
        rag_ok = rag_service.status().ready
        mic_ok = audio_manager.is_available
        ollama_ok = False
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=1.5)
            ollama_ok = r.status_code == 200
        except Exception:
            ollama_ok = False

        if db_ok and rag_ok and mic_ok and ollama_ok:
            return True, "All systems are operational, online, and ready."
        else:
            issues = []
            if not ollama_ok: issues.append("Local AI engine")
            if not mic_ok: issues.append("Microphone")
            if not db_ok: issues.append("Database")
            if not rag_ok: issues.append("Vector Index")
            return False, f"System warning: {', '.join(issues)} is currently degraded."

system_manager = SystemManager()
