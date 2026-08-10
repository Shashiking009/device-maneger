import os
import re
import subprocess
import platform
import ctypes
from typing import Dict, Any

# Windows Virtual Key Codes for Volume & Media
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

def press_vk_key(vk_code: int):
    try:
        ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0) # Key up
    except Exception as e:
        print("VK Key Error:", e)

def execute_automation_command(command: str) -> Dict[str, Any]:
    cmd = command.lower().strip()
    
    try:
        import pyautogui
        pyautogui.FAILSAFE = False
        has_pyautogui = True
    except ImportError:
        has_pyautogui = False

    # 1. Volume & Audio Controls
    if "volume up" in cmd or "louder" in cmd:
        for _ in range(5):
            press_vk_key(VK_VOLUME_UP)
        return {"status": "success", "message": "Increased volume."}

    if "volume down" in cmd or "lower volume" in cmd or "quiet" in cmd:
        for _ in range(5):
            press_vk_key(VK_VOLUME_DOWN)
        return {"status": "success", "message": "Decreased volume."}

    if "mute" in cmd or "unmute" in cmd:
        press_vk_key(VK_VOLUME_MUTE)
        return {"status": "success", "message": "Toggled volume mute."}

    if "play" in cmd or "pause" in cmd:
        press_vk_key(VK_MEDIA_PLAY_PAUSE)
        return {"status": "success", "message": "Toggled media playback."}

    # 2. Lock & Power Controls
    if "lock laptop" in cmd or "lock computer" in cmd or "lock screen" in cmd:
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        return {"status": "success", "message": "Locking your laptop workstation."}

    # 3. Window Controls
    if "switch window" in cmd or "next window" in cmd or "alt tab" in cmd:
        if has_pyautogui:
            pyautogui.hotkey('alt', 'tab')
        else:
            press_vk_key(0x12) # Alt
        return {"status": "success", "message": "Switched window."}

    if "minimize window" in cmd or "minimize" in cmd:
        if has_pyautogui:
            pyautogui.hotkey('win', 'down')
        return {"status": "success", "message": "Minimized window."}

    if "maximize window" in cmd or "maximize" in cmd:
        if has_pyautogui:
            pyautogui.hotkey('win', 'up')
        return {"status": "success", "message": "Maximized window."}

    if "close window" in cmd or "exit window" in cmd:
        if has_pyautogui:
            pyautogui.hotkey('alt', 'f4')
        return {"status": "success", "message": "Closed active window."}

    # 4. Keyboard Voice Typing
    type_match = re.search(r'(?:type|write|say)\s+(.+)', cmd)
    if type_match:
        text_to_type = type_match.group(1).strip()
        if has_pyautogui:
            pyautogui.write(text_to_type, interval=0.03)
            return {"status": "success", "message": f"Typed text: '{text_to_type}'"}
        else:
            return {"status": "error", "message": "PyAutoGUI not installed for typing."}

    if "press enter" in cmd or "hit enter" in cmd:
        if has_pyautogui:
            pyautogui.press('enter')
        return {"status": "success", "message": "Pressed Enter key."}

    if "press space" in cmd or "hit space" in cmd:
        if has_pyautogui:
            pyautogui.press('space')
        return {"status": "success", "message": "Pressed Spacebar."}

    if "select all" in cmd:
        if has_pyautogui:
            pyautogui.hotkey('ctrl', 'a')
        return {"status": "success", "message": "Selected all text."}

    if "copy" in cmd and "file" not in cmd and "folder" not in cmd:
        if has_pyautogui:
            pyautogui.hotkey('ctrl', 'c')
        return {"status": "success", "message": "Copied to clipboard."}

    if "paste" in cmd:
        if has_pyautogui:
            pyautogui.hotkey('ctrl', 'v')
        return {"status": "success", "message": "Pasted from clipboard."}

    return {"status": "unhandled"}

if __name__ == "__main__":
    res = execute_automation_command("volume up")
    print("Volume test:", res)
