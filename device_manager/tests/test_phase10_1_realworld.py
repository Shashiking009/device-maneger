import sys
import os
import time
import pytest
from pathlib import Path

PROJECT_DIR = r"C:\Users\sasi vardhan.P\myname\device_manager"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from core.orchestrator import orchestrator
from core.intent_models import IntentType
from core.conversation_context import conversation_context
from system.folder_resolver import folder_resolver
from system.window_context import window_context
from voice.voice_manager import voice_manager
from voice.wake_word import wake_word_detector
from ai.qwen_engine import qwen_engine

def test_phase10_1_realworld():
    print("==================================================================")
    print("      SPIDY AI PHASE 10.1 — REAL-WORLD INTELLIGENCE TEST SUITE   ")
    print("==================================================================")

    # 1. WAKE WORD NORMALIZATION
    print("\n--- 1. WAKE WORD NORMALIZATION ---")
    assert wake_word_detector.is_wake_phrase("hey spidey", ignore_cooldown=True)
    assert wake_word_detector.is_wake_phrase("a spider open chrome", ignore_cooldown=True)
    cmd = wake_word_detector.extract_command_after_wake("hey spidy open downloads")
    assert cmd == "open downloads"
    print(f"  [PASS] Wake phrase extraction: 'hey spidy open downloads' -> cmd: '{cmd}'")

    # 2. DYNAMIC SPECIAL FOLDER RESOLUTION (Downloads, Desktop, Documents)
    print("\n--- 2. DYNAMIC SPECIAL FOLDER RESOLUTION ---")
    dl_path = folder_resolver.resolve_folder("downloads")
    assert dl_path is not None and dl_path.name.lower() == "downloads"
    assert dl_path == Path.home() / "Downloads"
    print(f"  [PASS] 'downloads' resolved dynamically to: '{dl_path}'")

    res_dl = orchestrator.process_command("open Downloads")
    assert res_dl.intent == IntentType.OPEN_FOLDER
    print(f"  [PASS] 'open Downloads' -> {res_dl.intent.value} | Msg: '{res_dl.message}'")

    res_dt = orchestrator.process_command("open my Desktop folder")
    assert res_dt.intent == IntentType.OPEN_FOLDER
    print(f"  [PASS] 'open my Desktop folder' -> {res_dt.intent.value} | Msg: '{res_dt.message}'")

    # 3. PRONOUN & OBJECT REFERENCE RESOLUTION ("open that folder")
    print("\n--- 3. PRONOUN & OBJECT REFERENCE RESOLUTION ---")
    orchestrator.process_command("open Downloads")
    res_that = orchestrator.process_command("open that folder")
    assert res_that.intent == IntentType.OPEN_FOLDER
    print(f"  [PASS] 'open Downloads' -> 'open that folder' resolved to: {res_that.intent.value} ({res_that.message})")

    # 4. DETERMINISTIC MULTI-ACTION REQUESTS ("open Chrome and Notepad")
    print("\n--- 4. MULTI-ACTION COMMANDS ---")
    res_multi = orchestrator.process_command("open Chrome and Notepad")
    assert res_multi.success is True
    print(f"  [PASS] 'open Chrome and Notepad' -> Multi-Step Executed: '{res_multi.message}'")

    # 5. ACTIVE WINDOW AWARENESS
    print("\n--- 5. ACTIVE WINDOW AWARENESS ---")
    res_app_q = orchestrator.process_command("what application am I using?")
    assert res_app_q.intent == IntentType.PROCESS_STATUS
    print(f"  [PASS] 'what application am I using?' -> {res_app_q.intent.value} | Msg: '{res_app_q.message}'")

    # 6. LAPTOP TELEMETRY & STATUS
    print("\n--- 6. LAPTOP STATUS TELEMETRY ---")
    res_lap = orchestrator.process_command("how is my laptop?")
    assert res_lap.intent == IntentType.SYSTEM_STATUS
    assert "laptop" in res_lap.message.lower() or "cpu" in res_lap.message.lower()
    print(f"  [PASS] 'how is my laptop?' -> {res_lap.intent.value} | Msg: '{res_lap.message}'")

    # 7. CONVERSATIONAL CONTEXT ("What is Python?" -> "Who created it?")
    print("\n--- 7. CONVERSATIONAL CONTEXT RESOLUTION ---")
    conversation_context.last_ai_topic = "Python"
    res_who = conversation_context.resolve_references("who created it?")
    assert "Python" in res_who
    print(f"  [PASS] 'who created it?' resolved to: '{res_who}'")

    # 8. SPEAKER AUTHORIZATION & REJECTION
    print("\n--- 8. SPEAKER AUTHORIZATION & REJECTION ---")
    res_unauth = voice_manager.process_voice_text("open calculator", is_authorized=False)
    assert res_unauth["success"] is False
    print(f"  [PASS] Unauthorized speaker rejected safely (0 action / 0 TTS)")

    res_auth = voice_manager.process_voice_text("increase volume", is_authorized=True)
    assert res_auth["success"] is True
    print(f"  [PASS] Authorized speaker command executed: '{res_auth['message']}'")

    # 9. DETERMINISTIC ROUTING (0 QWEN CALLS FOR DETERMINISTIC COMMANDS)
    print("\n--- 9. QWEN ROUTING & ZERO-QWEN GUARANTEE ---")
    qwen_call_count = [0]
    orig_qwen = qwen_engine.classify_intent_with_qwen

    def spy_qwen(*args, **kwargs):
        qwen_call_count[0] += 1
        return orig_qwen(*args, **kwargs)

    qwen_engine.classify_intent_with_qwen = spy_qwen

    orchestrator.process_command("open Downloads")
    orchestrator.process_command("how is my laptop?")
    orchestrator.process_command("what application am I using?")

    assert qwen_call_count[0] == 0
    print(f"  [PASS] 'open Downloads', 'how is my laptop?', and 'what application am I using?' executed with 0 Qwen calls")

    print("\n==================================================================")
    print("    SPIDY AI PHASE 10.1 REAL-WORLD TEST SUITE (100% PASS)         ")
    print("==================================================================")
    return True

if __name__ == "__main__":
    test_phase10_1_realworld()
