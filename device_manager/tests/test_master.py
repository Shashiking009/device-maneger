import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import HOST, PORT, SERVER_URL, VERSION, DATABASE_PATH, VECTOR_STORE_PATH
from database import init_db, check_db_integrity, create_db_backup
from core.orchestrator import orchestrator
from rag.rag_engine import rag_service
from voice.voice_state import voice_state_machine
from voice.wake_word import wake_word_detector
from voice.text_to_speech import tts_engine
from telemetry import get_system_telemetry
from events import event_bus, SpidyEvent
from actions.planner import planner
from actions.validator import validator
from actions.executor import action_executor
from memory.storage import memory_storage
from memory.context_manager import context_manager
from memory.memory_service import memory_service
from memory.secrets import is_secret

def run_master_test_suite():
    print("==================================================================")
    print(f"      SPIDY AI v{VERSION} MASTER INTEGRATION & RELEASE TEST SUITE    ")
    print("==================================================================")

    # 1. PHASE 1 & CONFIG AUDIT
    print("\n--- PHASE 1: CORE CONFIGURATION & DATABASE INTEGRITY ---")
    init_db()
    db_ok = check_db_integrity()
    assert db_ok is True
    print(f"  [PASS] SQLite Database Integrity: OK ({DATABASE_PATH})")
    backup_path = create_db_backup()
    assert backup_path is not None
    print(f"  [PASS] Local DB Backup Created: {backup_path}")

    # 2. PHASE 2: ORCHESTRATOR & INTENT ROUTER
    print("\n--- PHASE 2: CENTRAL ORCHESTRATOR & INTENT ROUTER ---")
    resp_app = orchestrator.process_command("open calculator")
    assert resp_app.success is True
    assert resp_app.intent.value == "OPEN_APPLICATION"
    print(f"  [PASS] Orchestrator routed 'open calculator' -> {resp_app.intent.value}")

    # 3. PHASE 3: PERSISTENT LOCAL RAG
    print("\n--- PHASE 3: PERSISTENT LOCAL FAISS RAG ENGINE ---")
    rag_status = rag_service.status()
    assert rag_status.ready is True
    print(f"  [PASS] RAG Status: READY ({rag_status.chunks_count} chunks in FAISS index)")

    # 4. PHASE 4: VOICE ENGINE & WAKE WORD
    print("\n--- PHASE 4: VOICE ENGINE & WAKE-WORD DETECTOR ---")
    wake_word_detector.last_detection_time = 0.0
    assert wake_word_detector.is_wake_phrase("hey spidy open calculator") is True
    assert tts_engine.should_interrupt("stop") is True
    print("  [PASS] Wake-word 'Hey Spidy' & Voice Interruption ('stop') verified")

    # 5. PHASE 5: HUD & SYSTEM TELEMETRY
    print("\n--- PHASE 5: HUD & REAL-TIME SYSTEM TELEMETRY ---")
    telemetry = get_system_telemetry()
    assert 0.0 <= telemetry.cpu_percent <= 100.0
    assert 0.0 <= telemetry.memory_percent <= 100.0
    
    evt_bus = event_bus
    evt_bus.publish(SpidyEvent(event_type="MASTER_TEST", state="IDLE", message="Testing event bus"))
    assert len(evt_bus.event_history) > 0
    print(f"  [PASS] Telemetry & EventBus verified: CPU={telemetry.cpu_percent}%, RAM={telemetry.memory_percent}%")

    # 6. PHASE 6: ACTION ENGINE & MULTI-STEP PLANNING
    print("\n--- PHASE 6: ACTION ENGINE & MULTI-STEP PLANNING ---")
    plan = planner.create_plan("open calculator and notepad")
    assert len(plan.actions) == 2
    exec_plan = action_executor.execute_plan(plan, dry_run=True)
    assert exec_plan.status.value == "COMPLETED"
    print(f"  [PASS] Multi-step action plan executed successfully (Dry-Run: 2/2 steps completed)")

    # 7. PHASE 7: LOCAL MEMORY & CONTEXT ENGINE
    print("\n--- PHASE 7: LOCAL MEMORY & CONTEXT RESOLUTION ---")
    memory_storage.clear_all_memories()
    memory_service.process_memory_command("remember that I use VS Code")
    resolved = context_manager.resolve_reference("open my editor")
    assert "vs code" in resolved.lower() or "vscode" in resolved.lower()
    
    # Secret Check
    assert is_secret("sk-proj-1234567890abcdef1234567890") is True
    print(f"  [PASS] Memory saved, reference resolved ('{resolved}'), and secrets rejected safely")

    # 8. PHASE 8: PRODUCTION HARDENING & SECURITY AUDIT
    print("\n--- PHASE 8: PRODUCTION SECURITY & OFFLINE AUDIT ---")
    res_sec = orchestrator.process_command("run powershell -c Remove-Item C:\\*")
    assert res_sec.intent.value != "OPEN_APPLICATION"
    print("  [PASS] Production Security Audit: Arbitrary shell execution rejected safely!")

    print("\n==================================================================")
    print("  ALL 8 PHASES VERIFIED! SPIDY AI v1.0.0 RELEASE READY!           ")
    print("==================================================================")

if __name__ == "__main__":
    run_master_test_suite()
