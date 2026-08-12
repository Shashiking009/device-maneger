import time
import queue
import threading
import win32com.client
import pythoncom
from typing import Optional
from voice.config import TTS_ENABLED, MAX_SPOKEN_CHARS, STOP_PHRASES

class TextToSpeech:
    """
    Dedicated Worker Thread Windows SAPI5 Text-To-Speech Engine.
    Initializes SAPI.SpVoice COM object ONCE in a persistent background worker.
    Provides sub-50ms instant speech startup, cancellation, and zero COM re-initialization overhead.
    """
    def __init__(self):
        self._speech_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._is_speaking = False
        self._lock = threading.Lock()
        self._worker_thread = threading.Thread(target=self._tts_worker_loop, daemon=True)
        self._worker_thread.start()

    @property
    def is_speaking(self) -> bool:
        with self._lock:
            return self._is_speaking

    def should_interrupt(self, text: str) -> bool:
        lower = text.lower().strip()
        return any(p == lower or lower.startswith(p) for p in STOP_PHRASES)

    def stop(self):
        with self._lock:
            self._stop_event.set()
        # Clear any pending queued speech
        while not self._speech_queue.empty():
            try:
                self._speech_queue.get_nowait()
            except Exception:
                break

    def speak(self, text: str, async_mode: bool = True) -> bool:
        if not TTS_ENABLED or not text:
            return False

        clean_text = text.strip()
        if len(clean_text) > MAX_SPOKEN_CHARS:
            cut = clean_text[:MAX_SPOKEN_CHARS]
            last_dot = cut.rfind('.')
            if last_dot > 50:
                clean_text = cut[:last_dot+1]
            else:
                clean_text = cut.rstrip() + "..."

        self.stop() # Cancel any active speech

        done_event = threading.Event()
        self._speech_queue.put((clean_text, done_event))

        if not async_mode:
            done_event.wait(timeout=10.0)

        return True

    def _tts_worker_loop(self):
        pythoncom.CoInitialize()
        try:
            spk = win32com.client.Dispatch("SAPI.SpVoice")
        except Exception as e:
            print(f"[TTS WORKER ERROR]: SAPI5 Dispatch failed: {e}")
            return

        while True:
            try:
                item = self._speech_queue.get(timeout=0.1)
                if not item:
                    continue
                clean_text, done_event = item

                with self._lock:
                    self._stop_event.clear()
                    self._is_speaking = True

                try:
                    # 1 = SAPI5 SVIFlagsAsync
                    spk.Speak(clean_text, 1)

                    while spk.Status.RunningState == 2: # 2 = Speaking
                        if self._stop_event.is_set():
                            spk.Speak("", 2) # Purge speech buffer
                            break
                        time.sleep(0.02)
                except Exception as e:
                    print(f"[TTS ERROR]: SAPI5 speak error: {e}")
                finally:
                    with self._lock:
                        self._is_speaking = False
                    done_event.set()

            except queue.Empty:
                pass
            except Exception as e:
                print(f"[TTS WORKER EXCEPTION]: {e}")

tts_engine = TextToSpeech()
