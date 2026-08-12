import time
import datetime
import speech_recognition as sr
from typing import Tuple, Optional
from voice.config import LISTEN_TIMEOUT, MAX_LISTEN_SECONDS, AUDIO_ENERGY_THRESHOLD, PAUSE_THRESHOLD
from voice.audio_manager import audio_manager

def get_time_str() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

class SpeechToText:
    """
    Optimized Speech-To-Text engine utilizing SpeechRecognition.
    Uses 400ms pause threshold for fast end-of-speech detection and millisecond tracing.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = AUDIO_ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.pause_threshold = 0.4  # Fast end-of-speech detection
        self.recognizer.non_speaking_duration = 0.3

    def listen_and_recognize(
        self,
        timeout: float = LISTEN_TIMEOUT,
        phrase_time_limit: float = MAX_LISTEN_SECONDS
    ) -> Tuple[Optional[str], float]:
        if not audio_manager.is_available:
            audio_manager.check_microphone()
            if not audio_manager.is_available:
                return None, 0.0

        if not audio_manager.acquire_mic(timeout=1.5):
            return None, 0.0

        try:
            mic = sr.Microphone()
            with mic as source:
                self.recognizer.energy_threshold = AUDIO_ENERGY_THRESHOLD
                # print(f"[{get_time_str()}] [VOICE LISTEN START]")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            t_audio_rec = time.time()
            t_audio_str = get_time_str()
            print(f"[{t_audio_str}] [VOICE AUDIO RECEIVED]")

            print(f"[{get_time_str()}] [STT START]")
            t0 = time.time()
            text = self.recognizer.recognize_google(audio)
            dur_ms = round((time.time() - t0) * 1000, 2)
            t_stt_str = get_time_str()
            print(f"[{t_stt_str}] [STT COMPLETE] text='{text}' ({dur_ms}ms)")
            return text.strip(), 0.95
        except sr.WaitTimeoutError:
            return None, 0.0
        except sr.UnknownValueError:
            return "", 0.0
        except sr.RequestError as e:
            print(f"[{get_time_str()}] [STT ENGINE ERROR]: {e}")
            return None, 0.0
        except Exception as e:
            print(f"[{get_time_str()}] [STT GENERAL ERROR]: {e}")
            return None, 0.0
        finally:
            audio_manager.release_mic()

stt_engine = SpeechToText()
