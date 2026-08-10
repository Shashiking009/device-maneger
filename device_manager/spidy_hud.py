import sys
import os
import time
import json
import threading
import subprocess
import requests
import re
import math

import tkinter as tk
import win32com.client
import pythoncom

from config import SERVER_URL

HUD_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "hud_config.json")

def load_hud_position() -> tuple:
    try:
        if os.path.exists(HUD_CONFIG_PATH):
            with open(HUD_CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("x"), data.get("y")
    except Exception:
        pass
    return None, None

def save_hud_position(x: int, y: int):
    try:
        os.makedirs(os.path.dirname(HUD_CONFIG_PATH), exist_ok=True)
        with open(HUD_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"x": x, "y": y}, f)
    except Exception as e:
        print(f"[HUD CONFIG WARNING]: Could not save HUD position: {e}")

def show_windows_toast(title: str, message: str):
    ps_cmd = f'''
    [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
    $objNotifyIcon = New-Object System.Windows.Forms.NotifyIcon
    $objNotifyIcon.Icon = [System.Drawing.SystemIcons]::Information
    $objNotifyIcon.BalloonTipIcon = "Info"
    $objNotifyIcon.BalloonTipText = "{message}"
    $objNotifyIcon.BalloonTipTitle = "{title}"
    $objNotifyIcon.Visible = $True
    $objNotifyIcon.ShowBalloonTip(4000)
    '''
    try:
        subprocess.Popen(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

class SpidyCyberHUD:
    """
    Jarvis-Inspired Cyber Floating HUD for Spidy AI.
    Features state visualization, animated rings, WebSocket events, and telemetry display.
    Presentation layer only; delegates commands to SpidyOrchestrator backend.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spidy HUD")
        
        # Frameless, Always-On-Top, Transparent window
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.config(bg='#010206')
        self.root.wm_attributes("-transparentcolor", '#010206')

        # Window Position
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 320, 180
        saved_x, saved_y = load_hud_position()
        if saved_x is not None and saved_y is not None:
            x, y = saved_x, saved_y
        else:
            x, y = sw - w - 25, sh - h - 55
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Canvas for Spidy Cyber Core
        self.canvas = tk.Canvas(self.root, width=w, height=h, bg='#010206', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.center_x = w // 2
        self.center_y = 55
        self.pulse_phase = 0
        self.current_state = "IDLE"
        self.rotation_angle = 0

        # Visual Rings
        self.ring2 = self.canvas.create_oval(
            self.center_x - 42, self.center_y - 42,
            self.center_x + 42, self.center_y + 42,
            outline='#ff0055', width=2
        )
        self.ring1 = self.canvas.create_oval(
            self.center_x - 30, self.center_y - 30,
            self.center_x + 30, self.center_y + 30,
            outline='#00f0ff', width=3
        )
        self.core = self.canvas.create_oval(
            self.center_x - 20, self.center_y - 20,
            self.center_x + 20, self.center_y + 20,
            fill='#ff0055', outline='#ffffff', width=2
        )
        
        # Spidy Emblem
        self.icon = self.canvas.create_text(
            self.center_x, self.center_y,
            text="🕷️", font=("Segoe UI Emoji", 16), fill="#ffffff"
        )

        # Spidy HUD Labels
        self.status_label = self.canvas.create_text(
            self.center_x, 108,
            text="SPIDY ONLINE",
            font=("Orbitron", 10, "bold"), fill="#00f0ff"
        )
        self.sub_label = self.canvas.create_text(
            self.center_x, 128,
            text="Say 'Hey Spidy'...",
            font=("Consolas", 8), fill="#ff0055"
        )
        self.telemetry_label = self.canvas.create_text(
            self.center_x, 150,
            text="CPU: --% | RAM: --% | 🟢 LOCAL",
            font=("Consolas", 7), fill="#10b981"
        )

        # Window Dragging & Double Click Close
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Double-Button-1>", self.close_hud)

        # Start HUD Animations & Background Threads
        self.animate_hud()
        
        # Subscribe HUD to VoiceState Machine directly
        try:
            from voice.voice_state import voice_state_machine
            from voice.voice_manager import voice_manager
            voice_state_machine.subscribe(self.on_voice_event)
            voice_manager.start()
        except Exception as e:
            print(f"[HUD WARNING]: Local voice subsystem init warning: {e}")

        # Start Telemetry & WebSocket Reconnect Threads
        threading.Thread(target=self._telemetry_poll_loop, daemon=True).start()
        threading.Thread(target=self._websocket_reconnect_loop, daemon=True).start()

    def start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        save_hud_position(x, y)

    def close_hud(self, event=None):
        self.root.destroy()
        sys.exit(0)

    def update_hud(self, status: str, sub: str, color='#00f0ff'):
        self.current_state = status
        clean_sub = sub[:40] + "..." if len(sub) > 40 else sub
        self.canvas.itemconfig(self.status_label, text=status, fill=color)
        self.canvas.itemconfig(self.sub_label, text=clean_sub)

    def update_telemetry(self, text: str):
        self.canvas.itemconfig(self.telemetry_label, text=text)

    def animate_hud(self):
        self.pulse_phase = (self.pulse_phase + 1) % 20
        self.rotation_angle = (self.rotation_angle + 15) % 360

        state = self.current_state
        if state in ["LISTENING", "SPEAKING"]:
            r_offset = abs(10 - self.pulse_phase) * 1.2
        elif state in ["PROCESSING", "THINKING"]:
            r_offset = 3 + math.sin(self.rotation_angle * math.pi / 180) * 4
        else:
            r_offset = abs(10 - self.pulse_phase) * 0.5
        
        self.canvas.coords(
            self.ring2,
            self.center_x - 42 - r_offset, self.center_y - 42 - r_offset,
            self.center_x + 42 + r_offset, self.center_y + 42 + r_offset
        )
        self.root.after(60, self.animate_hud)

    def on_voice_event(self, event):
        state_colors = {
            "IDLE": "#00f0ff",
            "LISTENING": "#ff0055",
            "PROCESSING": "#eab308",
            "THINKING": "#eab308",
            "EXECUTING": "#10b981",
            "SPEAKING": "#a855f7",
            "ERROR": "#ef4444",
            "OFFLINE": "#6b7280"
        }
        color = state_colors.get(event.state.value, "#00f0ff")
        self.root.after(0, lambda: self.update_hud(event.state.value, event.message, color))

    def _telemetry_poll_loop(self):
        while True:
            try:
                res = requests.get(f"{SERVER_URL}/api/system", timeout=2)
                if res.status_code == 200:
                    data = res.json()
                    cpu = data.get("cpu_percent", 0.0)
                    ram = data.get("memory_percent", 0.0)
                    t_str = f"CPU: {cpu:.1f}% | RAM: {ram:.1f}% | 🟢 LOCAL"
                    self.root.after(0, lambda: self.update_telemetry(t_str))
            except Exception:
                pass
            time.sleep(2.0)

    def _websocket_reconnect_loop(self):
        backoff = 1
        ws_url = SERVER_URL.replace("http://", "ws://") + "/ws/spidy"
        
        while True:
            try:
                import websocket
                ws = websocket.WebSocketApp(
                    ws_url,
                    on_message=self._on_ws_message,
                    on_error=self._on_ws_error,
                    on_close=self._on_ws_close
                )
                ws.run_forever()
            except Exception:
                pass

            # Backoff before reconnecting
            self.root.after(0, lambda: self.update_hud("OFFLINE", "Backend Disconnected", "#6b7280"))
            time.sleep(backoff)
            backoff = min(backoff * 2, 16)

    def _on_ws_message(self, ws, message):
        try:
            data = json.loads(message)
            evt_type = data.get("event_type")
            state = data.get("state", "IDLE")
            msg = data.get("message", "")
            
            if evt_type == "VOICE_STATE_CHANGED":
                state_colors = {
                    "IDLE": "#00f0ff",
                    "LISTENING": "#ff0055",
                    "PROCESSING": "#eab308",
                    "EXECUTING": "#10b981",
                    "SPEAKING": "#a855f7",
                    "ERROR": "#ef4444"
                }
                color = state_colors.get(state, "#00f0ff")
                self.root.after(0, lambda: self.update_hud(state, msg, color))
        except Exception:
            pass

    def _on_ws_error(self, ws, error):
        pass

    def _on_ws_close(self, ws, close_status_code, close_msg):
        self.root.after(0, lambda: self.update_hud("OFFLINE", "Reconnecting...", "#6b7280"))

def run_spidy_hud():
    app = SpidyCyberHUD()
    app.root.mainloop()

if __name__ == "__main__":
    run_spidy_hud()
