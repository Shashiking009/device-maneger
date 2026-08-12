import os
import re
import json
import winreg
import subprocess
import platform
import psutil
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from config import DATA_DIR

APP_REGISTRY_CACHE = DATA_DIR / "app_registry.json"

class DiscoveredApp:
    def __init__(self, name: str, exec_path: str, aliases: List[str], launch_type: str = "exe"):
        self.name = name
        self.exec_path = exec_path
        self.aliases = aliases
        self.launch_type = launch_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "exec_path": self.exec_path,
            "aliases": self.aliases,
            "launch_type": self.launch_type
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DiscoveredApp":
        return cls(
            name=d["name"],
            exec_path=d["exec_path"],
            aliases=d["aliases"],
            launch_type=d.get("launch_type", "exe")
        )

class ApplicationManager:
    """
    Dynamic Windows Application Discovery & Execution Engine.
    Scans Start Menu, Registry App Paths, System Tools, and custom installs.
    """
    def __init__(self):
        self.apps: Dict[str, DiscoveredApp] = {}
        self.alias_map: Dict[str, str] = {}
        self.load_or_scan()

    def load_or_scan(self):
        if APP_REGISTRY_CACHE.exists():
            try:
                with open(APP_REGISTRY_CACHE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for app_dict in data.get("apps", []):
                        app = DiscoveredApp.from_dict(app_dict)
                        self.apps[app.name.lower()] = app
                        for alias in app.aliases:
                            self.alias_map[alias.lower()] = app.name.lower()
                if self.apps:
                    print(f"[APP MANAGER]: Loaded {len(self.apps)} apps from cache.")
                    return
            except Exception as e:
                print(f"[APP MANAGER WARNING]: Could not load app cache: {e}")

        self.scan_installed_applications()

    def scan_installed_applications(self) -> int:
        print("[APP MANAGER]: Scanning Windows applications...")
        found: Dict[str, DiscoveredApp] = {}

        # 1. Built-in System Tools
        system_tools = [
            ("Calculator", "calc.exe", ["calculator", "calc", "calculatorapp"]),
            ("Notepad", "notepad.exe", ["notepad", "note pad", "editor"]),
            ("File Explorer", "explorer.exe", ["explorer", "file explorer", "my computer", "this pc"]),
            ("Command Prompt", "cmd.exe", ["cmd", "command prompt", "terminal"]),
            ("Paint", "mspaint.exe", ["paint", "ms paint", "mspaint"]),
            ("Task Manager", "taskmgr.exe", ["task manager", "taskmgr"]),
            ("PowerShell", "powershell.exe", ["powershell"])
        ]
        for name, exe, aliases in system_tools:
            found[name.lower()] = DiscoveredApp(name, exe, aliases, launch_type="cmd")

        # 2. Registry App Paths
        for root_key in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for path_key in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
                             r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"]:
                try:
                    k = winreg.OpenKey(root_key, path_key)
                    count = winreg.QueryInfoKey(k)[0]
                    for i in range(count):
                        sub_name = winreg.EnumKey(k, i)
                        try:
                            sk = winreg.OpenKey(k, sub_name)
                            val, _ = winreg.QueryValueEx(sk, "")
                            if val and os.path.exists(val):
                                app_name = sub_name.replace(".exe", "").replace("_", " ").title()
                                alias_list = self._generate_aliases(app_name, sub_name)
                                found[app_name.lower()] = DiscoveredApp(app_name, val, alias_list, launch_type="file")
                        except Exception:
                            pass
                except Exception:
                    pass

        # 3. Start Menu Shortcuts (.lnk)
        start_menu_dirs = [
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs")
        ]
        for d in start_menu_dirs:
            if os.path.exists(d):
                for root, _, files in os.walk(d):
                    for f in files:
                        if f.endswith(".lnk"):
                            raw_name = f[:-4]
                            lnk_path = os.path.join(root, f)
                            alias_list = self._generate_aliases(raw_name, f)
                            found[raw_name.lower()] = DiscoveredApp(raw_name, lnk_path, alias_list, launch_type="file")

        # Save to memory and cache
        self.apps = found
        self.alias_map = {}
        for app in self.apps.values():
            for alias in app.aliases:
                self.alias_map[alias.lower()] = app.name.lower()

        try:
            with open(APP_REGISTRY_CACHE, "w", encoding="utf-8") as f:
                json.dump({"apps": [app.to_dict() for app in self.apps.values()]}, f, indent=2)
            print(f"[APP MANAGER]: Scanned & cached {len(self.apps)} applications.")
        except Exception as e:
            print(f"[APP MANAGER WARNING]: Failed to save cache: {e}")

        return len(self.apps)

    def _generate_aliases(self, display_name: str, filename: str) -> List[str]:
        aliases = set()
        clean_disp = display_name.lower().strip()
        clean_file = filename.replace(".exe", "").replace(".lnk", "").lower().strip()

        aliases.add(clean_disp)
        aliases.add(clean_file)

        # Specific alias additions
        if "chrome" in clean_disp:
            aliases.update(["chrome", "google chrome", "browser", "chrome browser"])
        elif "code" in clean_disp or "visual studio code" in clean_disp:
            aliases.update(["code", "vs code", "vscode", "visual studio code"])
        elif "antigravity" in clean_disp or "anti gravity" in clean_disp:
            aliases.update(["antigravity", "anti gravity", "anti-gravity"])
        elif "edge" in clean_disp:
            aliases.update(["edge", "msedge", "microsoft edge"])
        elif "notepad" in clean_disp:
            aliases.update(["notepad", "note pad"])
        elif "calculator" in clean_disp:
            aliases.update(["calculator", "calc"])

        # Strip common prefixes/suffixes
        stripped = re.sub(r"\b(google|microsoft|app|shortcut|desktop)\b", "", clean_disp).strip()
        if stripped and len(stripped) > 2:
            aliases.add(stripped)

        return list(aliases)

    def find_application(self, query: str) -> Optional[DiscoveredApp]:
        clean = query.lower().strip()
        clean = re.sub(r"\b(open|launch|start|run|show)\s+", "", clean).strip()

        # 1. Exact alias match
        if clean in self.alias_map:
            app_key = self.alias_map[clean]
            return self.apps.get(app_key)

        # 2. Exact app name match
        if clean in self.apps:
            return self.apps[clean]

        # 3. Partial / Substring match
        for app in self.apps.values():
            if clean in app.name.lower() or any(clean in a for a in app.aliases):
                return app

        return None

    def launch_application(self, query: str) -> Tuple[bool, str]:
        app = self.find_application(query)
        if not app:
            # Fallback to direct process name launch if Windows system tool
            clean_name = query.lower().strip().replace("open ", "").replace("launch ", "")
            try:
                os.startfile(f"{clean_name}.exe")
                return True, f"Launched '{clean_name}'."
            except Exception:
                return False, f"I couldn't find an installed application matching '{query}' on your system."

        try:
            if app.launch_type == "cmd":
                subprocess.Popen([app.exec_path], shell=True)
            else:
                os.startfile(app.exec_path)
            return True, f"Opening {app.name}."
        except Exception as e:
            return False, f"Failed to launch {app.name}: {str(e)}"

    def close_application(self, query: str) -> Tuple[bool, str]:
        clean = query.lower().strip().replace("close ", "").replace("quit ", "").replace("exit ", "").replace("stop ", "")
        app = self.find_application(clean)
        target_name = app.name if app else clean

        closed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pname = proc.info['name'].lower()
                if clean in pname or (app and any(a in pname for a in app.aliases)):
                    proc.terminate()
                    closed = True
            except Exception:
                pass

        if closed:
            return True, f"Closed {target_name}."
        else:
            return False, f"No running process found for '{target_name}'."

app_manager = ApplicationManager()
