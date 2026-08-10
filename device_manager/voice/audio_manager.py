import threading
import speech_recognition as sr

class AudioManager:
    """
    Microphone device detector and audio session manager.
    Prevents concurrent audio capture collisions and handles device unavailabilities.
    """
    def __init__(self):
        self._mic_lock = threading.Lock()
        self._is_available = False
        self.check_microphone()

    def check_microphone(self) -> bool:
        try:
            mics = sr.Microphone.list_microphone_names()
            self._is_available = len(mics) > 0
            return self._is_available
        except Exception as e:
            print(f"[AUDIO MANAGER WARNING]: Could not enumerate microphones: {e}")
            self._is_available = False
            return False

    @property
    def is_available(self) -> bool:
        return self._is_available

    def acquire_mic(self, timeout: float = 3.0) -> bool:
        return self._mic_lock.acquire(timeout=timeout)

    def release_mic(self):
        if self._mic_lock.locked():
            self._mic_lock.release()

audio_manager = AudioManager()
