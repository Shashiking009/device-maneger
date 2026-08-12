import win32gui
import win32con
import win32process
import psutil
from typing import Optional, List, Tuple

class WindowManager:
    """
    Windows Active Window Control & Focus Management Engine.
    Handles window focus switching, minimize, maximize, restore, close, and show desktop.
    """
    def get_active_window_title(self) -> str:
        try:
            hwnd = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(hwnd)
        except Exception:
            return ""

    def focus_window(self, app_name: str) -> Tuple[bool, str]:
        clean = app_name.lower().strip()
        matched_hwnd = None

        def enum_windows_callback(hwnd, extra):
            nonlocal matched_hwnd
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).lower()
                if title and clean in title:
                    matched_hwnd = hwnd

        try:
            win32gui.EnumWindows(enum_windows_callback, None)
            if matched_hwnd:
                win32gui.ShowWindow(matched_hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(matched_hwnd)
                return True, f"Switched to {app_name.title()}."
            return False, f"Could not find an open window matching '{app_name}'."
        except Exception as e:
            return False, f"Failed to switch window: {str(e)}"

    def minimize_active_window(self) -> Tuple[bool, str]:
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return True, "Minimized current window."
        except Exception as e:
            return False, f"Failed to minimize window: {e}"

    def maximize_active_window(self) -> Tuple[bool, str]:
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return True, "Maximized current window."
        except Exception as e:
            return False, f"Failed to maximize window: {e}"

    def restore_active_window(self) -> Tuple[bool, str]:
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            return True, "Restored window."
        except Exception as e:
            return False, f"Failed to restore window: {e}"

    def close_active_window(self) -> Tuple[bool, str]:
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return True, "Closed active window."
        except Exception as e:
            return False, f"Failed to close window: {e}"

    def show_desktop(self) -> Tuple[bool, str]:
        try:
            import win32com.client
            shell = win32com.client.Dispatch("Shell.Application")
            shell.ToggleDesktop()
            return True, "Showing desktop."
        except Exception:
            try:
                import pyautogui
                pyautogui.hotkey("win", "d")
                return True, "Showing desktop."
            except Exception as e:
                return False, f"Failed to show desktop: {e}"

window_manager = WindowManager()
