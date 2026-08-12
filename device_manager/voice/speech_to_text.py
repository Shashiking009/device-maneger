import time
import speech_recognition as sr
from typing import Tuple, Optional
from voice.config import LISTEN_TIMEOUT, MAX_LISTEN_SECONDS, AUDIO_ENERGY_THRESHOLD, PAUSE_THRESHOLD
from voice.audio_manager import audio_manager

class SpeechToText:
    """
    Robust Speech-To-Text engine utilizing SpeechRecognition.
    Enforces listening timeouts, phrase limits, and microphone error recovery.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = AUDIO_ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.pause_threshold = PAUSE_THRESHOLD

    def listen_and_recognize(
        self,
        timeout: float = LISTEN_TIMEOUT,
        phrase_time_limit: float = MAX_LISTEN_SECONDS
    ) -> Tuple[Optional[str], float]:
        if not audio_manager.is_available:
            audio_manager.check_microphone()
            if not audio_manager.is_available:
                return None, 0.0

        if not audio_manager.acquire_mic(timeout=2.0):
            return None, 0.0

        try:
            mic = sr.Microphone()
            with mic as source:
                self.recognizer.energy_threshold = 120
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            # Recognize using local/system engine
            text = self.recognizer.recognize_google(audio)
            return text.strip(), 0.95
        except sr.WaitTimeoutError:
            return None, 0.0
        except sr.UnknownValueError:
            return "", 0.0
        except sr.RequestError as e:
            print(f"[STT ENGINE ERROR]: Speech API error: {e}")
            return None, 0.0
        except Exception as e:
            print(f"[STT GENERAL ERROR]: Microphone capture error: {e}")
            return None, 0.0
        finally:
            audio_manager.release_mic()

stt_engine = SpeechToText()
