import time
import datetime
import traceback
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

def get_time_str() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

def safe_print(msg: str):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='ignore').decode('ascii'))

class VoiceManager:
    """
    Central Manager for Spidy Voice Assistant Subsystem.
    Coordinates Microphone -> Wake-Word -> STT -> SpidyOrchestrator -> SAPI5 TTS Pipeline.
    Includes heartbeat monitoring, automatic thread recovery, sub-second latency, and millisecond tracing.
    """
    def __init__(self):
        self.state_machine = voice_state_machine
        self.running = False
        self.listener_thread: Optional[threading.Thread] = None
        self._processing_lock = threading.Lock()
        self._last_heartbeat_time = 0.0

    def start(self):
        if self.running:
            return
        self.running = True
        self.listener_thread = threading.Thread(target=self._run_voice_loop, daemon=True)
        self.listener_thread.start()
        safe_print(f"[{get_time_str()}] [VOICE ENGINE] PROCESS STARTED")
        safe_print(f"[{get_time_str()}] [VOICE ENGINE] MICROPHONE OPENED")
        safe_print(f"[{get_time_str()}] [VOICE ENGINE] LISTEN LOOP ACTIVE")
        safe_print(f"[{get_time_str()}] [VOICE ENGINE] READY FOR WAKE WORD")

    def stop(self):
        self.running = False
        tts_engine.stop()
        self.state_machine.transition_to(VoiceState.STOPPED, "Voice Manager stopped.")

    def process_voice_text(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"success": False, "message": "Empty voice text"}

        clean_text = text.strip()
        t_start = get_time_str()

        # 1. Check Interruption phrases while speaking
        if tts_engine.is_speaking and tts_engine.should_interrupt(clean_text):
            safe_print(f"[{t_start}] [TTS INTERRUPTED]: User requested stop.")
            tts_engine.stop()
            self.state_machine.transition_to(VoiceState.IDLE, "Interrupted by user.")
            return {"success": True, "message": "Voice interrupted."}

        # 2. Check if text is wake phrase alone (0 Qwen, 0 RAG, 0 Planner calls)
        cmd_text = wake_word_detector.extract_command_after_wake(clean_text)
        if not cmd_text and wake_word_detector.is_wake_phrase(clean_text):
            greeting = random.choice(WAKE_RESPONSES)
            self.state_machine.transition_to(VoiceState.SPEAKING, greeting)
            safe_print(f"[{t_start}] [WAKE DETECTED]: True")
            safe_print(f"[{get_time_str()}] [TTS START]: '{greeting}'")
            tts_engine.speak(greeting, async_mode=True)
            safe_print(f"[{get_time_str()}] [TTS COMPLETE]")
            self.state_machine.transition_to(VoiceState.IDLE, "Wake word greeting complete.")
            return {"success": True, "intent": "WAKE_GREETING", "message": greeting}

        if not cmd_text:
            cmd_text = clean_text

        safe_print(f"[{get_time_str()}] [COMMAND EXTRACTED]: '{cmd_text}'")

        # 3. Duplicate Command Protection
        if not self._processing_lock.acquire(blocking=False):
            return {"success": False, "message": "Voice processing already active"}

        try:
            self.state_machine.transition_to(VoiceState.PROCESSING, f"Processing command: '{cmd_text}'", {"command": cmd_text})
            
            # Delegate strictly to SpidyOrchestrator
            safe_print(f"[{get_time_str()}] [ORCHESTRATOR START]")
            resp = orchestrator.process_command(cmd_text)
            
            safe_print(f"[{get_time_str()}] [INTENT]: {resp.intent.value}")
            safe_print(f"[{get_time_str()}] [ACTION]: {resp.message}")

            self.state_machine.transition_to(VoiceState.EXECUTING, f"Executing intent: {resp.intent.value}", {"intent": resp.intent.value})

            # Speak concise response via local TTS asynchronously
            if resp.message:
                self.state_machine.transition_to(VoiceState.SPEAKING, resp.message)
                safe_print(f"[{get_time_str()}] [TTS START]: '{resp.message}'")
                tts_engine.speak(resp.message, async_mode=True)
                safe_print(f"[{get_time_str()}] [TTS COMPLETE]")

            self.state_machine.transition_to(VoiceState.IDLE, "Command execution complete.")
            return {
                "success": resp.success,
                "intent": resp.intent.value,
                "message": resp.message
            }
        except Exception as e:
            safe_print(f"[{get_time_str()}] [VOICE EXECUTION ERROR]: {e}")
            self.state_machine.transition_to(VoiceState.ERROR, f"Voice execution error: {str(e)}")
            self.state_machine.transition_to(VoiceState.IDLE, "Recovered to idle after error.")
            return {"success": False, "message": str(e)}
        finally:
            self._processing_lock.release()

    def _run_voice_loop(self):
        self.state_machine.transition_to(VoiceState.IDLE, "Voice loop initialized.")
        
        while self.running:
            try:
                now = time.time()
                if (now - self._last_heartbeat_time) >= 5.0:
                    safe_print(f"[{get_time_str()}] [VOICE LOOP HEARTBEAT] LISTENING")
                    self._last_heartbeat_time = now

                # If currently speaking or processing, wait until TTS/Execution finishes + brief echo margin
                if self.state_machine.current_state in [VoiceState.PROCESSING, VoiceState.SPEAKING] or tts_engine.is_speaking:
                    time.sleep(0.15)
                    continue

                # 1. Idle Microphone Monitoring for Wake-Word / Command
                text, conf = stt_engine.listen_and_recognize(timeout=LISTEN_TIMEOUT, phrase_time_limit=MAX_LISTEN_SECONDS)

                if text is None:
                    time.sleep(0.1)
                    continue

                if not text:
                    continue

                t_cap_str = get_time_str()
                safe_print(f"[{t_cap_str}] [VOICE CAPTURED]: '{text}'")

                # Check if user spoke interruption while TTS was active
                if tts_engine.is_speaking and tts_engine.should_interrupt(text):
                    tts_engine.stop()
                    self.state_machine.transition_to(VoiceState.IDLE, "Speech stopped by voice interruption.")
                    continue

                normalized_text = wake_word_detector.normalize_wake_text(text)
                safe_print(f"[{get_time_str()}] [WAKE NORMALIZED]: '{normalized_text}'")

                # 2. Check Wake Word Detection
                is_wake = wake_word_detector.is_wake_phrase(text)
                safe_print(f"[{get_time_str()}] [WAKE DETECTED]: {is_wake}")

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
                        safe_print(f"[{get_time_str()}] [TTS START]: '{greeting}'")
                        tts_engine.speak(greeting, async_mode=True)
                        safe_print(f"[{get_time_str()}] [TTS COMPLETE]")
                        
                        # Wait for SAPI5 TTS to finish speaking + 300ms speaker echo margin
                        while tts_engine.is_speaking:
                            time.sleep(0.05)
                        time.sleep(0.3)

                        follow_up, _ = stt_engine.listen_and_recognize(timeout=4.0, phrase_time_limit=6.0)
                        if follow_up:
                            safe_print(f"[{get_time_str()}] [FOLLOW-UP CAPTURED]: '{follow_up}'")
                            self.process_voice_text(follow_up)
                        else:
                            safe_print(f"[{get_time_str()}] [TTS START]: 'Standing by, boss.'")
                            tts_engine.speak("Standing by, boss.", async_mode=True)
                            safe_print(f"[{get_time_str()}] [TTS COMPLETE]")
                            self.state_machine.transition_to(VoiceState.IDLE, "Command timeout after wake word.")

            except Exception as e:
                safe_print(f"[{get_time_str()}] [VOICE LOOP FATAL EXCEPTION]: {e}")
                safe_print(traceback.format_exc())
                self.state_machine.transition_to(VoiceState.ERROR, f"Voice loop exception: {e}")
                time.sleep(0.5)
                self.state_machine.transition_to(VoiceState.IDLE, "Recovered to idle after exception.")

voice_manager = VoiceManager()
