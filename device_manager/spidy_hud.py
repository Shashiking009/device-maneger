import sys
import os
import time
import threading
import subprocess
import requests
import re

import tkinter as tk

SERVER_URL = "http://127.0.0.1:8088"

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
        w, h = 280, 150
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
            self.center_x, 108,
            text="SPIDY ONLINE",
            font=("Orbitron", 10, "bold"), fill="#00f0ff"
        )
        self.sub_label = self.canvas.create_text(
            self.center_x, 128,
            text="Say 'Hey Spidy'...",
            font=("Consolas", 8), fill="#ff0055"
        )

        # Make HUD Draggable & Double click to close
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<Double-Button-1>", self.close_hud)

        # Start animation & background listener
        self.animate_hud()
        threading.Thread(target=self.start_voice_listener_thread, daemon=True).start()

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
        self.canvas.itemconfig(self.status_label, text=status, fill=color)
        self.canvas.itemconfig(self.sub_label, text=sub)

    def animate_hud(self):
        self.pulse_phase = (self.pulse_phase + 1) % 20
        r_offset = abs(10 - self.pulse_phase) * 0.7
        
        self.canvas.coords(
            self.ring2,
            self.center_x - 40 - r_offset, self.center_y - 40 - r_offset,
            self.center_x + 40 + r_offset, self.center_y + 40 + r_offset
        )
        self.root.after(70, self.animate_hud)

    def start_voice_listener_thread(self):
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        # High speed low latency parameters
        recognizer.energy_threshold = 250
        recognizer.dynamic_energy_threshold = False
        recognizer.pause_threshold = 0.5
        recognizer.operation_timeout = None
        
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

        while True:
            try:
                with mic as source:
                    # Capture fast 4-second audio phrase
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=4)

                try:
                    text = recognizer.recognize_google(audio)
                    print(f"[Spidy Captured]: '{text}'")
                    lower_text = text.lower()

                    wake_words = ["hey spidy", "hi spidy", "spidy", "spidey", "spider", "speedy", "ok spidy"]
                    if any(w in lower_text for w in wake_words):
                        self.update_hud("WAKE DETECTED", text, "#ff0055")

                        # INSTANT EXECUTION - NO SPOKEN DELAY
                        try:
                            res = requests.post(
                                f"{SERVER_URL}/api/voice/command",
                                json={"command": text},
                                timeout=4
                            )
                            if res.status_code == 200:
                                data = res.json()
                                msg = data.get("message", "Executed")
                                self.update_hud("EXECUTED", msg, "#10b981")
                        except Exception:
                            self.update_hud("ERROR", "Server Offline", "#ff0055")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass

            except Exception:
                time.sleep(0.5)

def run_spidy_hud():
    app = SpidyCyberHUD()
    app.root.mainloop()

if __name__ == "__main__":
    run_spidy_hud()
