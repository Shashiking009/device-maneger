import time
import threading
import win32com.client
import pythoncom
from typing import Optional
from voice.config import TTS_ENABLED, MAX_SPOKEN_CHARS, STOP_PHRASES

class TextToSpeech:
    """
    Non-blocking Windows SAPI5 Text-To-Speech engine.
    Supports speech cancellation/interruption, length limiting, and thread-safe COM initialization.
    """
    def __init__(self):
        self._speaking_thread = None
        self._stop_requested = False
        self._is_speaking = False
        self._lock = threading.Lock()

    @property
    def is_speaking(self) -> bool:
        with self._lock:
            return self._is_speaking

    def should_interrupt(self, text: str) -> bool:
        lower = text.lower().strip()
        return any(p == lower or lower.startswith(p) for p in STOP_PHRASES)

    def stop(self):
        with self._lock:
            self._stop_requested = True

    def speak(self, text: str, async_mode: bool = True) -> bool:
        if not TTS_ENABLED or not text:
            return False

        # Apply concise spoken length policy
        clean_text = text.strip()
        if len(clean_text) > MAX_SPOKEN_CHARS:
            # Cut at last sentence period before MAX_SPOKEN_CHARS
            cut = clean_text[:MAX_SPOKEN_CHARS]
            last_dot = cut.rfind('.')
            if last_dot > 50:
                clean_text = cut[:last_dot+1]
            else:
                clean_text = cut.rstrip() + "..."

        self.stop() # Interrupt any ongoing speech

        def _speak_task():
            with self._lock:
                self._stop_requested = False
                self._is_speaking = True

            try:
                pythoncom.CoInitialize()
                spk = win32com.client.Dispatch("SAPI.SpVoice")
                
                # Check for interruption before speaking
                if not self._stop_requested:
                    # SAPI5 Flags: 1 = SVIFlagsAsync
                    spk.Speak(clean_text, 1)

                    # Poll for completion or interruption signal
                    while spk.Status.RunningState == 2: # 2 = SAPI5 Speaking
                        if self._stop_requested:
                            spk.Speak("", 2) # Purge speech buffer
                            break
                        time.sleep(0.05)
            except Exception as e:
                print(f"[TTS WARNING]: SAPI5 speech error: {e}")
            finally:
                with self._lock:
                    self._is_speaking = False

        if async_mode:
            self._speaking_thread = threading.Thread(target=_speak_task, daemon=True)
            self._speaking_thread.start()
        else:
            _speak_task()

        return True

tts_engine = TextToSpeech()
