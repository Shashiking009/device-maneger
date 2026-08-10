import os
import sys

STARTUP_FOLDER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
DEVICE_MANAGER_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = sys.executable

VBS_SCRIPT_PATH = os.path.join(STARTUP_FOLDER, "Spidy_DeviceManager_Startup.vbs")
BAT_SCRIPT_PATH = os.path.join(DEVICE_MANAGER_DIR, "start_spidy_background.bat")

def install_startup():
    # 1. Create start_spidy_background.bat
    bat_content = f"""@echo off
cd /d "{DEVICE_MANAGER_DIR}"
start /b "" "{PYTHON_EXE}" -m uvicorn server:app --host 127.0.0.1 --port 8088
timeout /t 3 /nobreak >nul
start /b "" "{PYTHON_EXE}" spidy_listener.py
"""
    with open(BAT_SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"Created batch launcher at: {BAT_SCRIPT_PATH}")

    # 2. Create silent VBS script in Windows Startup Folder
    vbs_content = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{BAT_SCRIPT_PATH}" & chr(34), 0
Set WshShell = Nothing
"""
    with open(VBS_SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(vbs_content)
    print(f"Successfully installed Spidy Boot Launcher at: {VBS_SCRIPT_PATH}")
    print("\nSPIDY IS NOW CONFIGURED TO AUTO-START ON LAPTOP BOOT!")

def uninstall_startup():
    if os.path.exists(VBS_SCRIPT_PATH):
        os.remove(VBS_SCRIPT_PATH)
        print("Removed Spidy from Windows Startup.")
    else:
        print("Spidy startup script not found.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        uninstall_startup()
    else:
        install_startup()
