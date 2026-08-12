from capabilities.app_manager import app_manager, ApplicationManager
from capabilities.file_manager import file_manager, FileManager
from capabilities.window_manager import window_manager, WindowManager
from capabilities.system_manager import system_manager, SystemManager
from capabilities.keyboard_controller import keyboard_controller, KeyboardController

class CapabilityRegistry:
    """
    Central Capability Registry for Spidy AI.
    Unifies Windows Application Discovery, File Operations, Window Focus Control, System Telemetry, and Keyboard Control.
    """
    def __init__(self):
        self.apps = app_manager
        self.files = file_manager
        self.windows = window_manager
        self.system = system_manager
        self.keyboard = keyboard_controller

capability_registry = CapabilityRegistry()
