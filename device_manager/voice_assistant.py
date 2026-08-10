import os
import subprocess
import platform
import glob
import re
import psutil
from typing import Dict, Any

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_docs")
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWN_APPS = {
    "calculator": {
        "exec": ["calc.exe"],
        "processes": ["calc.exe", "calculatorapp.exe", "win32calc.exe", "calculator.exe"]
    },
    "notepad": {
        "exec": ["notepad.exe"],
        "processes": ["notepad.exe"]
    },
    "explorer": {
        "exec": ["explorer.exe"],
        "processes": ["explorer.exe"]
    },
    "file explorer": {
        "exec": ["explorer.exe"],
        "processes": ["explorer.exe"]
    },
    "cmd": {
        "exec": ["cmd.exe"],
        "processes": ["cmd.exe"]
    },
    "command prompt": {
        "exec": ["cmd.exe"],
        "processes": ["cmd.exe"]
    },
    "paint": {
        "exec": ["mspaint.exe"],
        "processes": ["mspaint.exe"]
    },
    "task manager": {
        "exec": ["taskmgr.exe"],
        "processes": ["taskmgr.exe"]
    },
    "browser": {
        "exec": ["start", "http://127.0.0.1:8088"],
        "processes": ["chrome.exe", "msedge.exe", "firefox.exe"]
    },
    "chrome": {
        "exec": ["chrome.exe"],
        "processes": ["chrome.exe"]
    },
    "edge": {
        "exec": ["msedge.exe"],
        "processes": ["msedge.exe"]
    },
    "vs code": {
        "exec": ["code"],
        "processes": ["code.exe"]
    },
    "code": {
        "exec": ["code"],
        "processes": ["code.exe"]
    }
}

KNOWN_FOLDERS = {
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "desktop": os.path.expanduser("~/Desktop"),
    "workspace": WORKSPACE_DIR,
    "uploads": UPLOAD_DIR
}

def close_application_process(app_name: str) -> bool:
    app_info = KNOWN_APPS.get(app_name.lower())
    target_procs = app_info["processes"] if app_info else [f"{app_name.lower()}.exe"]
    
    closed_any = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info['name'].lower() if proc.info['name'] else ""
            for target in target_procs:
                if target in pname or pname.startswith(app_name.lower()):
                    proc.kill()
                    closed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    if not closed_any and platform.system() == "Windows":
        for target in target_procs:
            try:
                subprocess.run(f"taskkill /f /im {target}", shell=True, capture_output=True)
                closed_any = True
            except Exception:
                pass
    return closed_any

from voice_automation import execute_automation_command

def execute_voice_command(command: str) -> Dict[str, Any]:
    cmd_lower = command.lower().strip()
    
    # Strip wake phrase 'hey spidy', 'hi spidy', 'spidy', 'spidey', 'spider'
    cmd_clean = re.sub(r'^(hey|hi|hello|ok|okay)?\s*(spidy|spidey|spider)\s*', '', cmd_lower).strip()
    if not cmd_clean:
        return {
            "status": "success",
            "action": "greeting",
            "message": "Hey! I am Spidy, your Cyber Voice Assistant. Say 'Hey Spidy open Calculator' or 'Hey Spidy close Calculator'."
        }

    # First check automation commands (volume, typing, power, windows)
    auto_res = execute_automation_command(cmd_clean)
    if auto_res["status"] != "unhandled":
        return auto_res

    # 1. Check for closing/killing applications
    close_match = re.search(r'(?:close|kill|exit|terminate|stop|shutdown)\s+(?:the\s+)?([a-zA-Z0-9_\-\s]+)', cmd_clean)
    if close_match:
        target_app = close_match.group(1).strip()
        closed = close_application_process(target_app)
        if closed:
            return {
                "status": "success",
                "action": "close_app",
                "app": target_app,
                "message": f"Successfully closed {target_app.title()} on your device."
            }
        else:
            return {
                "status": "warning",
                "action": "close_app",
                "app": target_app,
                "message": f"Tried to close {target_app.title()}, but no running process was found."
            }

    # 2. Check for opening applications
    for app_key, app_data in KNOWN_APPS.items():
        if f"open {app_key}" in cmd_clean or f"launch {app_key}" in cmd_clean or f"start {app_key}" in cmd_clean or cmd_clean == app_key:
            try:
                if platform.system() == "Windows":
                    subprocess.Popen(app_data["exec"], shell=True)
                else:
                    subprocess.Popen([app_data["exec"][0]])
                return {
                    "status": "success",
                    "action": "open_app",
                    "app": app_key,
                    "message": f"Opening {app_key.title()} on your device."
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Could not launch {app_key}: {str(e)}"
                }

    # 3. Check for opening folders
    for folder_key, folder_path in KNOWN_FOLDERS.items():
        if f"open {folder_key}" in cmd_clean or f"show {folder_key}" in cmd_clean:
            if os.path.exists(folder_path):
                try:
                    if platform.system() == "Windows":
                        os.startfile(folder_path)
                    else:
                        subprocess.Popen(["xdg-open", folder_path])
                    return {
                        "status": "success",
                        "action": "open_folder",
                        "folder": folder_key,
                        "message": f"Opening {folder_key.title()} folder."
                    }
                except Exception as e:
                    return {"status": "error", "message": f"Failed to open folder: {str(e)}"}

    # 4. Check for opening local files
    open_file_match = re.search(r'(?:open|launch|read|view)\s+(?:file|doc|document)?\s*([a-zA-Z0-9_\-\.\s]+)', cmd_clean)
    if open_file_match:
        target_name = open_file_match.group(1).strip()
        if target_name:
            search_dirs = [
                UPLOAD_DIR,
                WORKSPACE_DIR,
                r"C:\Users\sasi vardhan.P\.gemini\antigravity\brain\476a2db5-13c2-44bd-9c48-595dd8c6a927"
            ]
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
                    return {
                        "status": "success",
                        "action": "open_file",
                        "filename": filename,
                        "filepath": target_path,
                        "message": f"Opening file {filename}."
                    }
                except Exception as e:
                    return {"status": "error", "message": f"Error opening file: {str(e)}"}

    # 5. Check for system query commands
    if "system" in cmd_clean and ("status" in cmd_clean or "stats" in cmd_clean or "health" in cmd_clean):
        return {
            "status": "success",
            "action": "system_info",
            "message": "Checking system diagnostics. Check the system widget for real-time CPU and Memory stats."
        }

    # 6. Default: Treat as AI query to Qwen3 SLM
    return {
        "status": "ai_query",
        "query": cmd_clean,
        "message": f"Processing voice query with Qwen3 SLM: '{cmd_clean}'"
    }

if __name__ == "__main__":
    res = execute_voice_command("hey spidy open calculator")
    print("Open:", res)
    res_close = execute_voice_command("hey spidy close calculator")
    print("Close:", res_close)
