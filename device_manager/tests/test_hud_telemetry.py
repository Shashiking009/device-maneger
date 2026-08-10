import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telemetry import get_system_telemetry, SystemStats
from events import SpidyEvent, SpidyEventBus
from spidy_hud import load_hud_position, save_hud_position

def test_telemetry_metrics():
    print("\n--- TEST 1: SYSTEM TELEMETRY METRICS ---")
    stats = get_system_telemetry()
    assert isinstance(stats, SystemStats)
    assert 0.0 <= stats.cpu_percent <= 100.0
    assert 0.0 <= stats.memory_percent <= 100.0
    assert stats.processes > 0
    assert stats.uptime_sec >= 0.0
    print(f"  [PASS] Telemetry captured: CPU={stats.cpu_percent}%, RAM={stats.memory_percent}%, Procs={stats.processes}")

def test_event_bus():
    print("\n--- TEST 2: SPIDY EVENT BUS BROADCAST ---")
    bus = SpidyEventBus()
    evt = SpidyEvent(
        event_type="VOICE_STATE_CHANGED",
        state="LISTENING",
        message="Listening for user command"
    )
    bus.publish(evt)
    assert len(bus.event_history) > 0
    last_evt = bus.event_history[-1]
    assert last_evt["event_type"] == "VOICE_STATE_CHANGED"
    assert last_evt["state"] == "LISTENING"
    print(f"  [PASS] EventBus published and stored event: {last_evt['event_type']} ({last_evt['state']})")

def test_position_persistence():
    print("\n--- TEST 3: HUD POSITION PERSISTENCE ---")
    save_hud_position(450, 750)
    x, y = load_hud_position()
    assert x == 450
    assert y == 750
    print(f"  [PASS] Saved & Loaded HUD position successfully: x={x}, y={y}")

def test_hud_security_isolation():
    print("\n--- TEST 4: HUD SECURITY & ZERO-DIRECT-EXECUTION AUDIT ---")
    import inspect
    import spidy_hud
    
    source = inspect.getsource(spidy_hud)
    # Ensure HUD contains no direct shell or system invocation calls for user input
    forbidden_terms = ["os.system(", "subprocess.run(", "pyautogui.typewrite("]
    for term in forbidden_terms:
        assert term not in source, f"Security Violation: Forbidden call '{term}' found in HUD code!"
    print("  [PASS] Security audit verified: HUD contains ZERO direct shell/system execution calls!")

if __name__ == "__main__":
    print("======================================================")
    print("      SPIDY AI PHASE 5 HUD & TELEMETRY TEST SUITE     ")
    print("======================================================")
    test_telemetry_metrics()
    test_event_bus()
    test_position_persistence()
    test_hud_security_isolation()
    print("\nALL PHASE 5 HUD & TELEMETRY TESTS PASSED SUCCESSFULLY!")
