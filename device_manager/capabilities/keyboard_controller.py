import pyautogui
from typing import Tuple
from voice_automation import execute_automation_command

class KeyboardController:
    """
    Focused Window Voice Typing & Keyboard Controller.
    Sends text keystrokes or shortcut hotkeys strictly into the currently active Windows application.
    """
    def type_text(self, text: str) -> Tuple[bool, str]:
        if not text:
            return False, "No text provided to type."
        
        # Max length safety limit
        clean_text = text[:500]
        try:
            pyautogui.write(clean_text, interval=0.01)
            return True, f"Typed text into active window."
        except Exception as e:
            return False, f"Failed to type text: {str(e)}"

    def press_key(self, key_or_shortcut: str) -> Tuple[bool, str]:
        clean = key_or_shortcut.lower().strip()
        if clean in ["ctrl+c", "copy"]:
            succ, msg = execute_automation_command("copy")
            return succ, "Copied to clipboard." if succ else msg
        elif clean in ["ctrl+v", "paste"]:
            succ, msg = execute_automation_command("paste")
            return succ, "Pasted from clipboard." if succ else msg
        elif clean in ["ctrl+a", "select all"]:
            succ, msg = execute_automation_command("select all")
            return succ, "Selected all text." if succ else msg
        else:
            try:
                if "+" in clean:
                    keys = [k.strip() for k in clean.split("+")]
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(clean)
                return True, f"Pressed {clean}."
            except Exception as e:
                return False, f"Failed to press key '{clean}': {e}"

keyboard_controller = KeyboardController()
