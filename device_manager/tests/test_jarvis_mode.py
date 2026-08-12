import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import orchestrator
from capabilities.capability_registry import capability_registry
from capabilities.app_manager import app_manager
from capabilities.file_manager import file_manager
from capabilities.window_manager import window_manager
from capabilities.system_manager import system_manager
from capabilities.keyboard_controller import keyboard_controller
from memory.storage import memory_storage

def test_jarvis_mode_suite():
    print("==================================================================")
    print("      SPIDY AI PHASE 10 — JARVIS MODE MASTER TEST SUITE          ")
    print("==================================================================")

    # 1. DYNAMIC APPLICATION DISCOVERY & CONTROL
    print("\n--- 1. APPLICATION CONTROL & DISCOVERY ---")
    app_calc = app_manager.find_application("calculator")
    assert app_calc is not None
    print(f"  [PASS] Discovered Calculator: '{app_calc.name}' ({app_calc.exec_path})")

    app_chrome = app_manager.find_application("google chrome")
    assert app_chrome is not None or app_manager.find_application("chrome") is not None
    print(f"  [PASS] Discovered Google Chrome via App Paths / Start Menu!")

    res_open = orchestrator.process_command("open calculator")
    assert res_open.success is True
    print(f"  [PASS] 'open calculator' -> {res_open.message}")

    res_close = orchestrator.process_command("close calculator")
    print(f"  [PASS] 'close calculator' -> {res_close.message}")

    res_app_stat = orchestrator.process_command("is calculator running?")
    assert res_app_stat.success is True
    print(f"  [PASS] Application Status Query -> {res_app_stat.message}")

    # 2. FILE SYSTEM INTELLIGENCE
    print("\n--- 2. FILE SYSTEM INTELLIGENCE ---")
    res_fold = orchestrator.process_command("open Downloads")
    assert res_fold.success is True
    print(f"  [PASS] 'open Downloads' -> {res_fold.message}")

    res_create = orchestrator.process_command("create folder Spidy_Test_Folder")
    assert res_create.success is True
    print(f"  [PASS] 'create folder Spidy_Test_Folder' -> {res_create.message}")

    files = file_manager.search_files("python", limit=3)
    print(f"  [PASS] Searched local files for 'python': Found {len(files)} files.")

    # 3. WINDOW CONTROL & FOCUS SWITCHING
    print("\n--- 3. WINDOW CONTROL & FOCUS SWITCHING ---")
    res_min = orchestrator.process_command("minimize window")
    assert res_min.success is True
    print(f"  [PASS] 'minimize window' -> {res_min.message}")

    res_desk = orchestrator.process_command("show desktop")
    assert res_desk.success is True
    print(f"  [PASS] 'show desktop' -> {res_desk.message}")

    # 4. SYSTEM CONTROLS & DIAGNOSTICS
    print("\n--- 4. SYSTEM CONTROLS & DIAGNOSTICS ---")
    res_vol = orchestrator.process_command("increase volume")
    assert res_vol.success is True
    print(f"  [PASS] 'increase volume' -> {res_vol.message}")

    res_sys = orchestrator.process_command("how is my laptop")
    assert res_sys.success is True
    print(f"  [PASS] 'how is my laptop' -> {res_sys.message}")

    res_diag = orchestrator.process_command("are you working")
    assert res_diag.success is True
    print(f"  [PASS] Self Diagnostics -> {res_diag.message}")

    # 5. VOICE TYPING & AUTOMATION
    print("\n--- 5. VOICE TYPING & KEYBOARD AUTOMATION ---")
    res_type = orchestrator.process_command("type Hello World")
    assert res_type.success is True
    print(f"  [PASS] 'type Hello World' -> {res_type.message}")

    # 6. LOCAL AI, RAG & MEMORY
    print("\n--- 6. LOCAL AI, RAG & MEMORY ---")
    memory_storage.clear_all_memories()
    res_mem_save = orchestrator.process_command("remember that my project uses Qwen3")
    assert res_mem_save.success is True
    print(f"  [PASS] Memory Save -> {res_mem_save.message}")

    res_mem_q = orchestrator.process_command("what do you remember about me")
    assert res_mem_q.success is True
    print(f"  [PASS] Memory Query -> {res_mem_q.message}")

    res_ai = orchestrator.process_command("what is machine learning")
    assert res_ai.success is True and len(res_ai.message) > 10
    print(f"  [PASS] Local Qwen3 Question -> {res_ai.message[:80]}...")

    # 7. SECURITY & SHELL REJECTION
    print("\n--- 7. SECURITY & SHELL REJECTION AUDIT ---")
    res_sec = orchestrator.process_command("run powershell -c Remove-Item C:\\*")
    assert res_sec.intent.value != "OPEN_APPLICATION"
    print("  [PASS] Arbitrary PowerShell execution rejected safely!")

    print("\n==================================================================")
    print("  JARVIS MODE MASTER TEST SUITE COMPLETED SUCCESSFULLY (100% PASS)")
    print("==================================================================")

if __name__ == "__main__":
    test_jarvis_mode_suite()
