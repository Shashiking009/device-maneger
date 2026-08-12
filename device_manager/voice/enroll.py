import sys
import time
import numpy as np
from pathlib import Path

PROJECT_DIR = r"C:\Users\sasi vardhan.P\myname\device_manager"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

import speech_recognition as sr
from voice.speaker_verifier import speaker_verifier, EMBEDDING_FILE

def enroll_user_voice(num_samples: int = 5):
    print("==================================================================")
    print("        SPIDY AI — LOCAL VOICE IDENTITY ENROLLMENT CLI            ")
    print("==================================================================")
    print("\nThis utility will create your secure local speaker profile.")
    print("No raw audio files or embeddings will ever be uploaded to the cloud.\n")

    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 250

    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"[ERROR]: Could not initialize microphone: {e}")
        return False

    with mic as source:
        print("[MIC]: Calibrating background ambient noise level...")
        r.adjust_for_ambient_noise(source, duration=1.0)
        print("[MIC]: Calibration complete.\n")

    collected_embeddings = []
    phrase_prompt = "Hey Spidy, activate my assistant"

    for i in range(1, num_samples + 1):
        print(f"Sample {i}/{num_samples}: Please clearly say:")
        print(f"   --> \"{phrase_prompt}\"")
        print("Listening...")

        with mic as source:
            try:
                audio = r.listen(source, timeout=6.0, phrase_time_limit=4.0)
                raw_pcm = audio.get_raw_data(convert_rate=16000, convert_width=2)
                
                emb = speaker_verifier.extract_embedding(raw_pcm, sample_rate=16000)
                if emb is not None:
                    collected_embeddings.append(emb)
                    print(f"   [PASS] Sample {i} captured successfully!\n")
                else:
                    print("   [WARNING]: Audio sample was too quiet or short. Retrying...\n")
            except sr.WaitTimeoutError:
                print("   [WARNING]: Listening timed out. Retrying...\n")
            except Exception as e:
                print(f"   [ERROR]: Error capturing sample: {e}\n")

        time.sleep(0.5)

    if collected_embeddings:
        succ = speaker_verifier.save_enrolled_embedding(collected_embeddings)
        if succ:
            print("==================================================================")
            print("      VOICE ENROLLMENT COMPLETE! LOCAL PROFILE SECURED           ")
            print(f" Saved to: {EMBEDDING_FILE}")
            print("==================================================================")
            return True

    print("[FAILED]: Voice enrollment incomplete. Please re-run 'python -m voice.enroll'.")
    return False

if __name__ == "__main__":
    enroll_user_voice()
