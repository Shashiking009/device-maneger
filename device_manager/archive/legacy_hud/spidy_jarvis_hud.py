import sys
import os
import time
import threading
import subprocess
import requests
import re
import win32com.client

import tkinter as tk
from tkinter import font

# SAPI5 TTS Engine
try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
except Exception:
    speaker = None

def speak_jarvis(text):
    print(f"[JARVIS SPIDY VOICE]: {text}")
    if speaker:
        try:
            speaker.Speak(text)
        except Exception:
            pass

SERVER_URL = "http://127.0.0.1:8088"

class SpidyJarvisHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS Spidy HUD")
        
        # Make window frameless and topmost
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        # Transparent background keying on Windows
        self.root.config(bg='#010206')
        self.root.wm_attributes("-transparentcolor", '#010206')

        # Screen dimensions - position at bottom right
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 320, 180
        x, y = sw - w - 30, sh - h - 60
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Canvas for Arc Reactor / Mic Orb
        self.canvas = tk.Canvas(self.root, width=w, height=h, bg='#010206', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Drawing Glowing Arc Reactor Core
        self.center_x = w // 2
        self.center_y = 65
        self.radius = 35
        self.pulse_phase = 0
        self.is_listening = True

        # Draw outer cyan glowing rings
        self.ring2 = self.canvas.create_oval(
            self.center_x - 45, self.center_y - 45,
            self.center_x + 45, self.center_y + 45,
            outline='#00f0ff', width=2
        )
        self.ring1 = self.canvas.create_oval(
            self.center_x - 35, self.center_y - 35,
            self.center_x + 35, self.center_y + 35,
            outline='#a855f7', width=3
        )
        self.core = self.canvas.create_oval(
            self.center_x - 22, self.center_y - 22,
            self.center_x + 22, self.center_y + 22,
            fill='#00f0ff', outline='#ffffff', width=2
        )
        
        # Center Mic / Spider Symbol
        self.icon = self.canvas.create_text(
            self.center_x, self.center_y,
            text="🕷️", font=("Segoe UI Emoji", 18), fill="#ffffff"
        )

        # HUD Subtitle Labels
        self.status_label = self.canvas.create_text(
            self.center_x, 125,
            text="JARVIS SPIDY ONLINE",
            font=("Orbitron", 10, "bold"), fill="#00f0ff"
        )
        self.sub_label = self.canvas.create_text(
            self.center_x, 148,
            text="Say 'Hey Spidy' to command...",
            font=("Consolas", 8), fill="#a855f7"
        )

        # Make HUD Draggable
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

    def update_hud_text(self, status: str, sub: str, color='#00f0ff'):
        self.canvas.itemconfig(self.status_label, text=status, fill=color)
        self.canvas.itemconfig(self.sub_label, text=sub)

    def animate_hud(self):
        self.pulse_phase = (self.pulse_phase + 1) % 20
        r_offset = abs(10 - self.pulse_phase) * 0.8
        
        # Pulsing Arc Reactor Animation
        self.canvas.coords(
            self.ring2,
            self.center_x - 45 - r_offset, self.center_y - 45 - r_offset,
            self.center_x + 45 + r_offset, self.center_y + 45 + r_offset
        )
        
        self.root.after(80, self.animate_hud)

    def start_voice_listener_thread(self):
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 0.8
        mic = sr.Microphone()

        speak_jarvis("JARVIS Spidy system online. At your service, boss.")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)

        while True:
            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)

                try:
                    text = recognizer.recognize_google(audio)
                    print(f"[JARVIS Speech Captured]: '{text}'")
                    lower_text = text.lower()

                    wake_words = ["hey spidy", "hi spidy", "spidy", "spidey", "spider", "speedy", "ok spidy", "jarvis"]
                    if any(w in lower_text for w in wake_words):
                        self.update_hud_text("WAKE PHRASE DETECTED", f"Heard: '{text}'", "#ff007f")
                        speak_jarvis("At your service, boss.")

                        try:
                            res = requests.post(
                                f"{SERVER_URL}/api/voice/command",
                                json={"command": text},
                                timeout=10
                            )
                            if res.status_code == 200:
                                data = res.json()
                                msg = data.get("message", "Task completed.")
                                self.update_hud_text("TASK EXECUTED", msg, "#10b981")
                                speak_jarvis(msg)
                        except Exception:
                            speak_jarvis("Server connection lost.")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass

            except Exception:
                time.sleep(1)

def run_jarvis():
    hud = SpidyJarvisHUD()
    hud.root.mainloop()

if __name__ == "__main__":
    run_jarvis()
