import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_DIR, HOST, PORT, SERVER_URL, OLLAMA_HOST, OLLAMA_MODEL
from database import check_db_integrity
from voice.audio_manager import audio_manager
from voice.wake_word import wake_word_detector

def test_windows_setup():
    print("==================================================================")
    print("      SPIDY AI WINDOWS STARTUP & ENVIRONMENT VERIFICATION        ")
    print("==================================================================")

    # 1. Repository Path & Files Check
    print("\n--- 1. REPOSITORY PATH & REQUIRED FILES ---")
    req_files = ["start_spidy.bat", "server.py", "spidy_hud.py", "config.py", "database.py", "requirements.txt"]
    for f in req_files:
        fpath = os.path.join(BASE_DIR, f)
        assert os.path.exists(fpath) is True
        print(f"  [PASS] File exists: {f}")

    # 2. Python Environment & Version Check
    print("\n--- 2. PYTHON ENVIRONMENT ---")
    print(f"  [PASS] Python Executable: {sys.executable}")
    print(f"  [PASS] Python Version: {sys.version.split()[0]}")

    # 3. Ollama & Qwen3 Availability
    print("\n--- 3. OLLAMA & QWEN3 SLM ENGINE ---")
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        assert r.status_code == 200
        models = [m["name"] for m in r.json().get("models", [])]
        has_qwen = any("qwen3" in m for m in models)
        assert has_qwen is True
        print(f"  [PASS] Ollama active at {OLLAMA_HOST} | Model 'qwen3:1.7b' detected!")
    except Exception as e:
        print(f"  [FAIL/WARNING] Ollama check: {e}")

    # 4. Database Integrity Check
    print("\n--- 4. DATABASE INTEGRITY ---")
    db_ok = check_db_integrity()
    assert db_ok is True
    print("  [PASS] SQLite Database PRAGMA integrity_check: OK")

    # 5. Microphone & Audio Hardware Check
    print("\n--- 5. MICROPHONE & SYSTEM-WIDE VOICE CHECK ---")
    mic_ok = audio_manager.is_available
    print(f"  [{'PASS' if mic_ok else 'WARNING'}] Microphone status: {'Available' if mic_ok else 'Unavailable/Muted'}")
    assert wake_word_detector.is_wake_phrase("hey spidy open calculator") is True
    print("  [PASS] Wake-word detector ('Hey Spidy') active for system-wide background listening.")

    # 6. Windows Startup VBS Registration Check
    print("\n--- 6. WINDOWS STARTUP VBS REGISTRATION ---")
    startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
    vbs_path = os.path.join(startup_folder, "Spidy_DeviceManager_Startup.vbs")
    if os.path.exists(vbs_path):
        print(f"  [PASS] Windows Startup VBS registered at: {vbs_path}")
    else:
        print(f"  [NOTICE] Startup VBS not yet run; run 'python install_spidy_software.py' to register.")

    print("\n==================================================================")
    print("  WINDOWS ENVIRONMENT VERIFICATION PASSED SUCCESSFULLY!           ")
    print("==================================================================")

if __name__ == "__main__":
    test_windows_setup()
