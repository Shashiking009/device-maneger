import sys
import os
import time
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voice.models import VoiceState, VoiceEvent
from voice.voice_state import voice_state_machine
from voice.wake_word import wake_word_detector
from voice.text_to_speech import tts_engine
from voice.voice_manager import voice_manager
from core.intent_models import IntentType

def test_voice_state_machine():
    print("\n--- TEST 1: VOICE STATE MACHINE TRANSITIONS ---")
    history = []
    def record_event(evt: VoiceEvent):
        history.append(evt.state)

    voice_state_machine.subscribe(record_event)
    voice_state_machine.transition_to(VoiceState.LISTENING)
    voice_state_machine.transition_to(VoiceState.PROCESSING)
    voice_state_machine.transition_to(VoiceState.IDLE)

    assert VoiceState.LISTENING in history
    assert VoiceState.PROCESSING in history
    assert VoiceState.IDLE in history
    print(f"  [PASS] State machine transitions recorded: {[h.value for h in history]}")

def test_wake_word_detector():
    print("\n--- TEST 2: WAKE WORD DETECTOR & ALIAS EXTRACTION ---")
    wake_word_detector.last_detection_time = 0.0 # reset cooldown
    assert wake_word_detector.is_wake_phrase("hey spidy open calculator") is True
    
    cmd = wake_word_detector.extract_command_after_wake("hey spidy, what is machine learning?")
    assert cmd == "what is machine learning?"

    # Rejection of non-wake phrase
    wake_word_detector.last_detection_time = 0.0
    assert wake_word_detector.is_wake_phrase("good morning computer") is False
    print(f"  [PASS] Wake phrase 'Hey Spidy' detected and command extracted: '{cmd}'")

def test_tts_and_interruption():
    print("\n--- TEST 3: TTS & VOICE INTERRUPTION ---")
    assert tts_engine.should_interrupt("stop") is True
    assert tts_engine.should_interrupt("quiet") is True
    assert tts_engine.should_interrupt("tell me more") is False
    print("  [PASS] Interruption phrases ('stop', 'quiet') matched successfully")

def test_voice_pipeline_orchestrator_integration():
    print("\n--- TEST 4: VOICE MANAGER -> ORCHESTRATOR PIPELINE ---")
    # Test App Control
    res_app = voice_manager.process_voice_text("hey spidy open calculator")
    assert res_app.get("success") is True
    assert res_app.get("intent") == IntentType.OPEN_APPLICATION.value
    print(f"  [PASS] Voice command 'open calculator' -> {res_app.get('intent')}")

    # Test AI Question
    res_ai = voice_manager.process_voice_text("hey spidy what is python")
    assert res_ai.get("success") is True
    assert res_ai.get("intent") in [IntentType.AI_QUESTION.value, IntentType.RAG_QUERY.value]
    print(f"  [PASS] Voice query 'what is python' -> {res_ai.get('intent')}")

    # Test RAG Query
    res_rag = voice_manager.process_voice_text("hey spidy what does my project plan say about Qwen3")
    assert res_rag.get("success") is True
    assert res_rag.get("intent") == IntentType.RAG_QUERY.value
    print(f"  [PASS] Voice query 'my project plan...' -> {res_rag.get('intent')}")

def test_voice_security():
    print("\n--- TEST 5: VOICE SECURITY & PROMPT INJECTION CONTAINMENT ---")
    res_sec = voice_manager.process_voice_text("hey spidy run shell command rm -rf /")
    assert res_sec.get("intent") not in [IntentType.OPEN_APPLICATION.value, IntentType.CLOSE_APPLICATION.value]
    print(f"  [PASS] Malicious voice command contained safely -> {res_sec.get('intent')}")

if __name__ == "__main__":
    print("======================================================")
    print("      SPIDY AI PHASE 4 VOICE ENGINE TEST SUITE       ")
    print("======================================================")
    test_voice_state_machine()
    test_wake_word_detector()
    test_tts_and_interruption()
    test_voice_pipeline_orchestrator_integration()
    test_voice_security()
    print("\nALL PHASE 4 VOICE TESTS PASSED SUCCESSFULLY!")
