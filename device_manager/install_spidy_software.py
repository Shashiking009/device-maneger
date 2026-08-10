import os
import sys
import subprocess
import win32com.client

STARTUP_FOLDER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
DESKTOP_FOLDER = os.path.expanduser("~/Desktop")
DEVICE_MANAGER_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = sys.executable

BAT_SCRIPT_PATH = os.path.join(DEVICE_MANAGER_DIR, "start_spidy_background.bat")
VBS_STARTUP_PATH = os.path.join(STARTUP_FOLDER, "Spidy_DeviceManager_Startup.vbs")

def create_desktop_shortcut():
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_path = os.path.join(DESKTOP_FOLDER, "Device Manager Spidy AI.lnk")
    shortcut = shell.CreateShortCut(shortcut_path)
    
    # Points to batch launcher
    shortcut.TargetPath = BAT_SCRIPT_PATH
    shortcut.WorkingDirectory = DEVICE_MANAGER_DIR
    shortcut.Description = "Device Manager & Hands-Free Spidy Voice AI Assistant"
    shortcut.WindowStyle = 7 # Minimized
    shortcut.IconLocation = r"C:\Windows\System32\shell32.dll,14" # Microchip / AI icon
    shortcut.save()
    print(f"Created Desktop Shortcut: {shortcut_path}")

def setup_boot_startup():
    bat_content = f"""@echo off
cd /d "{DEVICE_MANAGER_DIR}"
start /b "" "{PYTHON_EXE}" -m uvicorn server:app --host 127.0.0.1 --port 8088
timeout /t 3 /nobreak >nul
start /b "" "{PYTHON_EXE}" spidy_listener.py
start "" "http://127.0.0.1:8088"
"""
    with open(BAT_SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(bat_content)

    vbs_content = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{BAT_SCRIPT_PATH}" & chr(34), 0
Set WshShell = Nothing
"""
    with open(VBS_STARTUP_PATH, "w", encoding="utf-8") as f:
        f.write(vbs_content)
    print(f"Configured Windows Startup: {VBS_STARTUP_PATH}")

if __name__ == "__main__":
    print("\n=======================================================")
    print(" INSTALLING DEVICE MANAGER & SPIDY DESKTOP SOFTWARE")
    print("=======================================================\n")
    setup_boot_startup()
    create_desktop_shortcut()
    print("\nSUCCESS! Device Manager & Spidy AI installed on your laptop.")
