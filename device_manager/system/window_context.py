import os
import psutil
from typing import Dict, Any, Optional

try:
    import win32gui
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class WindowContextDetector:
    """
    Active Foreground Window Awareness Engine.
    Inspects currently focused window title, process name, and application type.
    Enables focused voice typing and context-aware queries ("What app am I using?").
    """
    def __init__(self):
        pass

    def get_active_window_info(self) -> Dict[str, Any]:
        if not HAS_WIN32:
            return {
                "title": "Unknown Window",
                "process_name": "unknown.exe",
                "app_alias": "Unknown",
                "pid": 0
            }

        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return {
                    "title": "Desktop / No Active Window",
                    "process_name": "explorer.exe",
                    "app_alias": "Desktop",
                    "pid": 0
                }

            title = win32gui.GetWindowText(hwnd) or "Untitled Window"
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            pname = "unknown.exe"
            try:
                proc = psutil.Process(pid)
                pname = proc.name().lower()
            except Exception:
                pass

            # Resolve user-friendly alias
            alias = self._resolve_app_alias(pname, title)

            return {
                "title": title,
                "process_name": pname,
                "app_alias": alias,
                "pid": pid,
                "hwnd": hwnd
            }
        except Exception as e:
            return {
                "title": f"Error: {e}",
                "process_name": "unknown.exe",
                "app_alias": "Unknown",
                "pid": 0
            }

    def _resolve_app_alias(self, pname: str, title: str) -> str:
        pname_lower = pname.lower()
        title_lower = title.lower()

        if "chrome" in pname_lower or "chrome" in title_lower:
            return "Google Chrome"
        elif "code" in pname_lower or "visual studio code" in title_lower:
            return "VS Code"
        elif "notepad" in pname_lower or "notepad" in title_lower:
            return "Notepad"
        elif "calc" in pname_lower or "calculator" in title_lower:
            return "Calculator"
        elif "explorer" in pname_lower:
            return "File Explorer"
        elif "cmd" in pname_lower or "powershell" in title_lower or "windows terminal" in title_lower:
            return "Terminal"
        elif "msedge" in pname_lower:
            return "Microsoft Edge"
        else:
            # Fall back to capitalized executable basename
            base = pname_lower.replace(".exe", "").capitalize()
            return base if base else "Active Window"

window_context = WindowContextDetector()
