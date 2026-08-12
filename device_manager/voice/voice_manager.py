import time
import threading
import random
from typing import Optional, Callable, Dict, Any
from voice.config import WAKE_WORD, WAKE_WORD_ALIASES, LISTEN_TIMEOUT, MAX_LISTEN_SECONDS, STOP_PHRASES, WAKE_RESPONSES
from voice.models import VoiceState, VoiceEvent
from voice.voice_state import voice_state_machine
from voice.audio_manager import audio_manager
from voice.wake_word import wake_word_detector
from voice.speech_to_text import stt_engine
from voice.text_to_speech import tts_engine
from core.orchestrator import orchestrator

def safe_print(msg: str):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='ignore').decode('ascii'))

class VoiceManager:
    """
    Central Manager for Spidy Voice Assistant Subsystem.
    Coordinates Microphone -> Wake-Word -> STT -> SpidyOrchestrator -> TTS Pipeline.
    Voice layer converts Audio<->Text only; all intent processing is delegated to SpidyOrchestrator.
    """
    def __init__(self):
        self.state_machine = voice_state_machine
        self.running = False
        self.listener_thread: Optional[threading.Thread] = None
        self._processing_lock = threading.Lock()

    def start(self):
        if self.running:
            return
        self.running = True
        self.listener_thread = threading.Thread(target=self._run_voice_loop, daemon=True)
        self.listener_thread.start()
        print("[VOICE MANAGER]: Background Voice Loop active.")

    def stop(self):
        self.running = False
        tts_engine.stop()
        self.state_machine.transition_to(VoiceState.STOPPED, "Voice Manager stopped.")

    def process_voice_text(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"success": False, "message": "Empty voice text"}

        clean_text = text.strip()

        # 1. Check Interruption phrases while speaking
        if tts_engine.is_speaking and tts_engine.should_interrupt(clean_text):
            safe_print("[TTS INTERRUPTED]: User requested stop.")
            tts_engine.stop()
            self.state_machine.transition_to(VoiceState.IDLE, "Interrupted by user.")
            return {"success": True, "message": "Voice interrupted."}

        # 2. Check if text is wake phrase alone
        cmd_text = wake_word_detector.extract_command_after_wake(clean_text)
        if not cmd_text and wake_word_detector.is_wake_phrase(clean_text):
            greeting = random.choice(WAKE_RESPONSES)
            self.state_machine.transition_to(VoiceState.SPEAKING, greeting)
            safe_print(f"[WAKE DETECTED]: True")
            safe_print(f"[TTS START]: '{greeting}'")
            tts_engine.speak(greeting, async_mode=False)
            safe_print(f"[TTS COMPLETE]")
            self.state_machine.transition_to(VoiceState.IDLE, "Wake word greeting complete.")
            return {"success": True, "intent": "WAKE_GREETING", "message": greeting}

        if not cmd_text:
            cmd_text = clean_text

        safe_print(f"[COMMAND EXTRACTED]: '{cmd_text}'")

        # 3. Duplicate Command Protection
        if not self._processing_lock.acquire(blocking=False):
            return {"success": False, "message": "Voice processing already active"}

        try:
            self.state_machine.transition_to(VoiceState.PROCESSING, f"Processing command: '{cmd_text}'", {"command": cmd_text})
            
            # Delegate strictly to SpidyOrchestrator
            resp = orchestrator.process_command(cmd_text)
            
            safe_print(f"[INTENT]: {resp.intent.value}")
            safe_print(f"[ACTION]: {resp.message}")

            self.state_machine.transition_to(VoiceState.EXECUTING, f"Executing intent: {resp.intent.value}", {"intent": resp.intent.value})

            # Speak concise response via local TTS
            if resp.message:
                self.state_machine.transition_to(VoiceState.SPEAKING, resp.message)
                safe_print(f"[TTS START]: '{resp.message}'")
                tts_engine.speak(resp.message, async_mode=False)
                safe_print(f"[TTS COMPLETE]")

            self.state_machine.transition_to(VoiceState.IDLE, "Command execution complete.")
            return {
                "success": resp.success,
                "intent": resp.intent.value,
                "message": resp.message
            }
        except Exception as e:
            safe_print(f"[VOICE EXECUTION ERROR]: {e}")
            self.state_machine.transition_to(VoiceState.ERROR, f"Voice execution error: {str(e)}")
            self.state_machine.transition_to(VoiceState.IDLE, "Recovered to idle after error.")
            return {"success": False, "message": str(e)}
        finally:
            self._processing_lock.release()

    def _run_voice_loop(self):
        self.state_machine.transition_to(VoiceState.IDLE, "Voice loop initialized.")
        
        while self.running:
            try:
                # If currently speaking or processing, sleep briefly
                if self.state_machine.current_state in [VoiceState.PROCESSING, VoiceState.SPEAKING]:
                    time.sleep(0.2)
                    continue

                # 1. Idle Microphone Monitoring for Wake-Word / Command
                text, conf = stt_engine.listen_and_recognize(timeout=LISTEN_TIMEOUT, phrase_time_limit=MAX_LISTEN_SECONDS)

                if text is None:
                    time.sleep(0.3)
                    continue

                if not text:
                    continue

                safe_print(f"[VOICE CAPTURED]: '{text}'")

                # Check if user spoke interruption while TTS was active
                if tts_engine.is_speaking and tts_engine.should_interrupt(text):
                    tts_engine.stop()
                    self.state_machine.transition_to(VoiceState.IDLE, "Speech stopped by voice interruption.")
                    continue

                normalized_text = wake_word_detector.normalize_wake_text(text)
                safe_print(f"[WAKE NORMALIZED]: '{normalized_text}'")

                # 2. Check Wake Word Detection
                is_wake = wake_word_detector.is_wake_phrase(text)
                safe_print(f"[WAKE DETECTED]: {is_wake}")

                if is_wake:
                    self.state_machine.transition_to(VoiceState.LISTENING, "Wake word 'Hey Spidy' detected!", {"raw_text": text})
                    
                    cmd_extracted = wake_word_detector.extract_command_after_wake(text)
                    
                    # If command was spoken in same utterance as wake word
                    if cmd_extracted:
                        self.process_voice_text(cmd_extracted)
                    else:
                        # Spoke wake word alone -> speak JARVIS greeting and listen for follow-up command
                        greeting = random.choice(WAKE_RESPONSES)
                        self.state_machine.transition_to(VoiceState.SPEAKING, greeting)
                        safe_print(f"[TTS START]: '{greeting}'")
                        tts_engine.speak(greeting, async_mode=False)
                        safe_print(f"[TTS COMPLETE]")
                        
                        follow_up, _ = stt_engine.listen_and_recognize(timeout=5.0, phrase_time_limit=8.0)
                        if follow_up:
                            safe_print(f"[FOLLOW-UP CAPTURED]: '{follow_up}'")
                            self.process_voice_text(follow_up)
                        else:
                            safe_print(f"[TTS START]: 'Standing by, boss.'")
                            tts_engine.speak("Standing by, boss.", async_mode=False)
                            safe_print(f"[TTS COMPLETE]")
                            self.state_machine.transition_to(VoiceState.IDLE, "Command timeout after wake word.")

            except Exception as e:
                safe_print(f"[VOICE LOOP ERROR]: {e}")
                self.state_machine.transition_to(VoiceState.ERROR, f"Voice loop exception: {e}")
                time.sleep(1.0)
                self.state_machine.transition_to(VoiceState.IDLE, "Recovered to idle.")

voice_manager = VoiceManager()
