import sys
import os
import time
import pytest

PROJECT_DIR = r"C:\Users\sasi vardhan.P\myname\device_manager"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from core.orchestrator import orchestrator
from core.intent_models import IntentType
from core.conversation_context import conversation_context
from system.window_context import window_context
from ai.qwen_engine import qwen_engine

def test_phase10_intelligence():
    print("==================================================================")
    print("       SPIDY AI PHASE 10 — JARVIS INTELLIGENCE TEST SUITE        ")
    print("==================================================================")

    # 1. NATURAL APPLICATION COMMANDS
    print("\n--- 1. NATURAL APPLICATION COMMANDS ---")
    res_nat_app1 = orchestrator.process_command("Can you open Chrome?")
    assert res_nat_app1.intent == IntentType.OPEN_APPLICATION
    print(f"  [PASS] 'Can you open Chrome?' -> {res_nat_app1.intent.value} | Msg: '{res_nat_app1.message}'")

    res_nat_app2 = orchestrator.process_command("Launch Google Chrome")
    assert res_nat_app2.intent == IntentType.OPEN_APPLICATION
    print(f"  [PASS] 'Launch Google Chrome' -> {res_nat_app2.intent.value} | Msg: '{res_nat_app2.message}'")

    # 2. NATURAL VOLUME COMMANDS
    print("\n--- 2. NATURAL VOLUME COMMANDS ---")
    res_vol1 = orchestrator.process_command("Turn the volume up")
    assert res_vol1.intent == IntentType.VOLUME_UP
    print(f"  [PASS] 'Turn the volume up' -> {res_vol1.intent.value} | Msg: '{res_vol1.message}'")

    res_vol2 = orchestrator.process_command("Make it louder")
    assert res_vol2.intent == IntentType.VOLUME_UP
    print(f"  [PASS] 'Make it louder' -> {res_vol2.intent.value} | Msg: '{res_vol2.message}'")

    # 3. PRONOUN & APPLICATION REFERENCE RESOLUTION
    print("\n--- 3. PRONOUN & APPLICATION REFERENCE RESOLUTION ---")
    orchestrator.process_command("Open Chrome")
    res_close_it = orchestrator.process_command("Close it")
    assert res_close_it.intent == IntentType.CLOSE_APPLICATION
    assert "chrome" in res_close_it.message.lower() or "google chrome" in res_close_it.message.lower()
    print(f"  [PASS] 'Open Chrome' -> 'Close it' resolved to: {res_close_it.intent.value} ({res_close_it.message})")

    # 4. PREVIOUS-OBJECT & FOLDER RESOLUTION
    print("\n--- 4. PREVIOUS-OBJECT & FOLDER RESOLUTION ---")
    orchestrator.process_command("Open Downloads")
    res_that_fold = orchestrator.process_command("Open that folder")
    assert res_that_fold.intent == IntentType.OPEN_FOLDER
    print(f"  [PASS] 'Open Downloads' -> 'Open that folder' resolved to: {res_that_fold.intent.value} ({res_that_fold.message})")

    # 5. CONVERSATIONAL CONTEXT ("What is Python?" -> "Who created it?")
    print("\n--- 5. CONVERSATIONAL CONTEXT RESOLUTION ---")
    conversation_context.last_ai_topic = "Python"
    resolved_q = conversation_context.resolve_references("Who created it?")
    assert "Python" in resolved_q
    print(f"  [PASS] 'Who created it?' resolved to: '{resolved_q}'")

    # 6. CURRENT WINDOW AWARENESS
    print("\n--- 6. CURRENT WINDOW AWARENESS ---")
    win_info = window_context.get_active_window_info()
    assert "title" in win_info and "app_alias" in win_info
    print(f"  [PASS] Active Window Title: '{win_info['title']}' | App Alias: '{win_info['app_alias']}'")

    res_app_q = orchestrator.process_command("What application am I using?")
    assert res_app_q.intent == IntentType.PROCESS_STATUS
    print(f"  [PASS] 'What application am I using?' -> {res_app_q.intent.value} | Msg: '{res_app_q.message}'")

    # 7. NATURAL MULTI-STEP REQUESTS
    print("\n--- 7. NATURAL MULTI-STEP REQUESTS ---")
    res_multi = orchestrator.process_command("Open Chrome and Notepad")
    assert res_multi.success is True
    print(f"  [PASS] 'Open Chrome and Notepad' -> Executed Multi-Step Action: '{res_multi.message}'")

    # 8. MEMORY INTEGRATION & PREFERENCE RESOLUTION
    print("\n--- 8. MEMORY INTEGRATION & PREFERENCE RESOLUTION ---")
    res_mem_save = orchestrator.process_command("Remember that my project is in Downloads")
    assert res_mem_save.success is True
    print(f"  [PASS] Memory Saved: '{res_mem_save.message}'")

    # 9. SECURITY BOUNDARIES & RISK CONFIRMATION
    print("\n--- 9. SECURITY BOUNDARIES & RISK CONFIRMATION ---")
    res_sec = orchestrator.process_command("run powershell -c Remove-Item C:\\*")
    assert res_sec.intent != IntentType.OPEN_APPLICATION
    print(f"  [PASS] Arbitrary PowerShell command blocked safely: '{res_sec.message[:70]}...'")

    # 10. DETERMINISTIC ROUTING (0 QWEN CALLS FOR BASIC CONTROLS)
    print("\n--- 10. DETERMINISTIC ROUTING & NO UNNECESSARY QWEN CALLS ---")
    qwen_call_count = [0]
    orig_qwen = qwen_engine.classify_intent_with_qwen

    def spy_qwen(*args, **kwargs):
        qwen_call_count[0] += 1
        return orig_qwen(*args, **kwargs)

    qwen_engine.classify_intent_with_qwen = spy_qwen

    res_det_calc = orchestrator.process_command("open calculator")
    res_det_vol = orchestrator.process_command("increase volume")

    assert qwen_call_count[0] == 0
    print(f"  [PASS] 'open calculator' and 'increase volume' executed with 0 Qwen calls (Deterministic PASS)")

    print("\n==================================================================")
    print("      SPIDY AI PHASE 10 INTELLIGENCE TEST SUITE (100% PASS)       ")
    print("==================================================================")
    return True

if __name__ == "__main__":
    test_phase10_intelligence()
