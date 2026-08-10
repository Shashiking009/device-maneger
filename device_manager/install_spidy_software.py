import os
import sys
import win32com.client
from config import HOST, PORT, BASE_DIR

STARTUP_FOLDER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
DEVICE_MANAGER_DIR = str(BASE_DIR)
BAT_SCRIPT_PATH = os.path.join(DEVICE_MANAGER_DIR, "start_spidy.bat")
VBS_STARTUP_PATH = os.path.join(STARTUP_FOLDER, "Spidy_DeviceManager_Startup.vbs")

shell = win32com.client.Dispatch("WScript.Shell")

ACTIVE_DESKTOP = shell.SpecialFolders("Desktop")
USER_DESKTOP = os.path.expanduser("~/Desktop")
ONEDRIVE_DESKTOP = os.path.expanduser("~/OneDrive/Desktop")

def create_desktop_shortcut():
    desktop_dirs = set([ACTIVE_DESKTOP, USER_DESKTOP, ONEDRIVE_DESKTOP])
    for d in desktop_dirs:
        if os.path.exists(d):
            shortcut_path = os.path.join(d, "Device Manager Spidy AI.lnk")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = BAT_SCRIPT_PATH
            shortcut.WorkingDirectory = DEVICE_MANAGER_DIR
            shortcut.Description = "Spidy AI v1.0.0 Cyber Assistant"
            shortcut.WindowStyle = 1 # Normal Window
            shortcut.IconLocation = r"C:\Windows\System32\shell32.dll,14"
            shortcut.save()
            print(f"  [SUCCESS] Created Spidy Desktop Shortcut at: {shortcut_path}")

def setup_boot_startup():
    vbs_content = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{BAT_SCRIPT_PATH}" & chr(34), 0
Set WshShell = Nothing
"""
    with open(VBS_STARTUP_PATH, "w", encoding="utf-8") as f:
        f.write(vbs_content)
    print(f"  [SUCCESS] Configured Windows Startup VBS at: {VBS_STARTUP_PATH}")

if __name__ == "__main__":
    print("\n=======================================================")
    print("      INSTALLING SPIDY AI v1.0.0 WINDOWS SETUP")
    print("=======================================================\n")
    setup_boot_startup()
    create_desktop_shortcut()
    print("\nSUCCESS! Spidy AI Windows Startup & Desktop Shortcuts Configured.")
