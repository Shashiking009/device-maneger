import time
import requests
import json
import re
import os
import sys
import subprocess
import win32com.client

# Windows native text-to-speech engine
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    print(f"[Spidy Voice Output]: {text}")
    try:
        speaker.Speak(text)
    except Exception as e:
        print("TTS Error:", e)

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

SERVER_URL = "http://127.0.0.1:8088"

def check_server_health():
    try:
        res = requests.get(f"{SERVER_URL}/api/system", timeout=2)
        return res.status_code == 200
    except Exception:
        return False

def listen_and_process():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.8
    mic = sr.Microphone()

    print("\n=======================================================")
    print(" [SPIDY] SYSTEM-WIDE VOICE LISTENER ACTIVE")
    print(" Wake Phrase: 'Hey Spidy' (Works from ANY window)")
    print("=======================================================\n")
    
    show_windows_toast("Spidy Voice Active", "Spidy is listening for 'Hey Spidy' from any window!")
    speak("Spidy System-Wide Voice Assistant active. Say Hey Spidy followed by your command.")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)

            try:
                text = recognizer.recognize_google(audio)
                print(f"[Captured Audio]: '{text}'")
                lower_text = text.lower()

                # Phonetic variants of 'hey spidy'
                wake_words = ["hey spidy", "hi spidy", "spidy", "spidey", "spider", "speedy", "sweetie spidy", "ok spidy"]
                if any(w in lower_text for w in wake_words):
                    print(f"-> WAKE PHRASE DETECTED in '{text}'")
                    show_windows_toast("Spidy Awakened!", f"Heard: {text}")
                    speak("Hey! I'm listening.")

                    # Execute command via Device Manager Server API
                    try:
                        res = requests.post(
                            f"{SERVER_URL}/api/voice/command",
                            json={"command": text},
                            timeout=10
                        )
                        if res.status_code == 200:
                            data = res.json()
                            msg = data.get("message", "Task completed.")
                            show_windows_toast("Spidy Task Executed", msg)
                            speak(msg)
                    except Exception as err:
                        speak("Sorry, Device Manager server is not responding.")

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Speech Recognition service error:", e)

        except Exception as e:
            time.sleep(1)

if __name__ == "__main__":
    attempts = 0
    while not check_server_health() and attempts < 15:
        print("Waiting for Device Manager server on startup...")
        time.sleep(2)
        attempts += 1

    listen_and_process()
