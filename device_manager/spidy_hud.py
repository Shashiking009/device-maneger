import sys
import os
import time
import threading
import subprocess
import requests
import re
import win32com.client

import tkinter as tk

import pythoncom

def speak_text_async(text):
    def _speak_thread():
        try:
            pythoncom.CoInitialize()
            spk = win32com.client.Dispatch("SAPI.SpVoice")
            spk.Speak(text, 1)
        except Exception as e:
            print("SAPI5 TTS Warning:", e)
    threading.Thread(target=_speak_thread, daemon=True).start()

def show_windows_toast(title: str, message: str):
    ps_cmd = f'''
    [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
    $objNotifyIcon = New-Object System.Windows.Forms.NotifyIcon
    $objNotifyIcon.Icon = [System.Drawing.SystemIcons]::Information
    $objNotifyIcon.BalloonTipIcon = "Info"
    $objNotifyIcon.BalloonTipText = "{message}"
    $objNotifyIcon.BalloonTipTitle = "{title}"
    $objNotifyIcon.Visible = $True
    $objNotifyIcon.ShowBalloonTip(5000)
    '''
    try:
        subprocess.Popen(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

from config import SERVER_URL

class SpidyCyberHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spidy HUD")
        
        # Make window frameless, transparent, and topmost
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        # Transparent background keying on Windows
        self.root.config(bg='#010206')
        self.root.wm_attributes("-transparentcolor", '#010206')

        # Position in bottom right corner
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 300, 160
        x, y = sw - w - 25, sh - h - 55
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Canvas for Cyber Spidy Orb
        self.canvas = tk.Canvas(self.root, width=w, height=h, bg='#010206', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.center_x = w // 2
        self.center_y = 55
        self.pulse_phase = 0

        # Futuristic Spidy Hologram Rings
        self.ring2 = self.canvas.create_oval(
            self.center_x - 40, self.center_y - 40,
            self.center_x + 40, self.center_y + 40,
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
        
        # Spidy Spider Emblem
        self.icon = self.canvas.create_text(
            self.center_x, self.center_y,
            text="🕷️", font=("Segoe UI Emoji", 16), fill="#ffffff"
        )

        # Spidy HUD Labels
        self.status_label = self.canvas.create_text(
            self.center_x, 110,
            text="SPIDY ONLINE",
            font=("Orbitron", 10, "bold"), fill="#00f0ff"
        )
        self.sub_label = self.canvas.create_text(
            self.center_x, 132,
            text="Say 'Hey Spidy'...",
            font=("Consolas", 8), fill="#ff0055"
        )

        # Make HUD Draggable & Double click to close
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<Double-Button-1>", self.close_hud)

        # Start animation & background listener
        self.animate_hud()
        from voice.voice_state import voice_state_machine
        from voice.voice_manager import voice_manager
        
        # Subscribe HUD to VoiceState transitions
        voice_state_machine.subscribe(self.on_voice_event)
        voice_manager.start()

    def start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def close_hud(self, event=None):
        self.root.destroy()
        sys.exit(0)

    def update_hud(self, status: str, sub: str, color='#00f0ff'):
        clean_sub = sub[:42] + "..." if len(sub) > 42 else sub
        self.canvas.itemconfig(self.status_label, text=status, fill=color)
        self.canvas.itemconfig(self.sub_label, text=clean_sub)

    def animate_hud(self):
        self.pulse_phase = (self.pulse_phase + 1) % 20
        r_offset = abs(10 - self.pulse_phase) * 0.7
        
        self.canvas.coords(
            self.ring2,
            self.center_x - 40 - r_offset, self.center_y - 40 - r_offset,
            self.center_x + 40 + r_offset, self.center_y + 40 + r_offset
        )
        self.root.after(70, self.animate_hud)

    def on_voice_event(self, event):
        state_colors = {
            "IDLE": "#00f0ff",
            "LISTENING": "#ff0055",
            "PROCESSING": "#eab308",
            "EXECUTING": "#10b981",
            "SPEAKING": "#a855f7",
            "ERROR": "#ef4444",
            "STOPPED": "#6b7280"
        }
        color = state_colors.get(event.state.value, "#00f0ff")
        self.root.after(0, lambda: self.update_hud(event.state.value, event.message, color))
        if event.state.value in ["EXECUTING", "SPEAKING"] and event.message:
            show_windows_toast("Spidy Response", event.message)

def run_spidy_hud():
    app = SpidyCyberHUD()
    app.root.mainloop()

if __name__ == "__main__":
    run_spidy_hud()
