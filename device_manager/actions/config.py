import os

# Action Engine Parameters
ACTION_TIMEOUT = 10.0      # max seconds per single action
MAX_RETRIES = 1           # retry limit for recoverable actions
MAX_PLAN_STEPS = 5        # max actions per multi-step plan
DRY_RUN = False           # if True, validate without executing
MAX_TYPED_TEXT_LENGTH = 500

# Controlled Allow-Lists
ALLOWED_APPLICATIONS = {
    "calculator": ["calc.exe", "calculatorapp.exe", "calculator.exe"],
    "notepad": ["notepad.exe"],
    "explorer": ["explorer.exe"],
    "file explorer": ["explorer.exe"],
    "cmd": ["cmd.exe"],
    "command prompt": ["cmd.exe"],
    "paint": ["mspaint.exe"],
    "task manager": ["taskmgr.exe"],
    "chrome": ["chrome.exe"],
    "edge": ["msedge.exe"],
    "browser": ["msedge.exe", "chrome.exe"],
    "code": ["code.exe", "code"],
    "vs code": ["code.exe", "code"]
}

ALLOWED_KEYS = {
    "enter", "esc", "space", "tab", "backspace", "delete",
    "up", "down", "left", "right", "home", "end",
    "pageup", "pagedown", "f1", "f2", "f5", "f11"
}

ALLOWED_HOTKEYS = {
    ("ctrl", "c"), ("ctrl", "v"), ("ctrl", "a"), ("ctrl", "s"),
    ("ctrl", "z"), ("ctrl", "f"), ("alt", "tab"), ("alt", "f4"),
    ("win", "d"), ("win", "e"), ("win", "r")
}
