import os
import sys
import subprocess
import win32com.client

STARTUP_FOLDER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
DEVICE_MANAGER_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = sys.executable

shell = win32com.client.Dispatch("WScript.Shell")

# Get active Windows desktop path (handles OneDrive Desktop)
ACTIVE_DESKTOP = shell.SpecialFolders("Desktop")
USER_DESKTOP = os.path.expanduser("~/Desktop")
ONEDRIVE_DESKTOP = os.path.expanduser("~/OneDrive/Desktop")

BAT_SCRIPT_PATH = os.path.join(DEVICE_MANAGER_DIR, "start_spidy_background.bat")
VBS_STARTUP_PATH = os.path.join(STARTUP_FOLDER, "Spidy_DeviceManager_Startup.vbs")

def create_desktop_shortcut():
    desktop_dirs = set([ACTIVE_DESKTOP, USER_DESKTOP, ONEDRIVE_DESKTOP])
    for d in desktop_dirs:
        if os.path.exists(d):
            shortcut_path = os.path.join(d, "Device Manager Spidy AI.lnk")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = BAT_SCRIPT_PATH
            shortcut.WorkingDirectory = DEVICE_MANAGER_DIR
            shortcut.Description = "Device Manager & Hands-Free Spidy Voice AI Assistant"
            shortcut.WindowStyle = 7 # Minimized
            shortcut.IconLocation = r"C:\Windows\System32\shell32.dll,14" # Microchip / AI icon
            shortcut.save()
            print(f"Created Desktop Shortcut at: {shortcut_path}")

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
    setup_boot_startup()
    create_desktop_shortcut()
    print("SUCCESS! Device Manager & Spidy AI shortcut installed on active Desktop.")
