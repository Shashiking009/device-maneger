import time
import json
import requests
from typing import Dict, Any, Optional, Tuple
from config import OLLAMA_HOST, OLLAMA_MODEL

class QwenEngine:
    """
    Interface to local Ollama C++ runtime running Qwen3 SLM.
    Handles AI question responses and intent classification fallback.
    """
    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        self.host = host
        self.model = model

    def classify_intent_with_qwen(self, user_input: str) -> Optional[Dict[str, Any]]:
        prompt = f"""You are an intent classification assistant for Spidy AI.
Given the user input, return ONLY a valid JSON object classifying the intent.

Supported Intent Names:
- OPEN_APPLICATION (target: app name like calculator, notepad, chrome, vs code, etc.)
- CLOSE_APPLICATION (target: app name)
- TYPE_TEXT (target: text string to type)
- KEY_PRESS (target: enter, space, tab, backspace, etc.)
- COPY
- PASTE
- VOLUME_UP
- VOLUME_DOWN
- MUTE
- UNMUTE
- LOCK_SYSTEM
- OPEN_FOLDER (target: downloads, documents, desktop, workspace, uploads)
- OPEN_FILE (target: filename)
- SYSTEM_STATUS
- AI_QUESTION (for general knowledge questions, programming help, explanations)
- UNKNOWN

User Input: "{user_input}"

JSON Output:
"""
        try:
            res = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1}
                },
                timeout=1.5
            )
            if res.status_code == 200:
                raw_text = res.json().get("response", "").strip()
                # Extract JSON block
                json_start = raw_text.find("{")
                json_end = raw_text.rfind("}")
                if json_start != -1 and json_end != -1:
                    json_str = raw_text[json_start:json_end+1]
                    data = json.loads(json_str)
                    return data
        except Exception as e:
            print("Qwen Intent Classifier Error:", e)
        return None

    def generate_ai_response(self, prompt: str, temperature: float = 0.7) -> Tuple[str, float]:
        start_t = time.time()
        try:
            res = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature}
                },
                timeout=120
            )
            if res.status_code == 200:
                data = res.json()
                reply = data.get("response", "").strip()
                total_duration_ns = data.get("total_duration", 0)
                eval_count = data.get("eval_count", 0)
                tps = round((eval_count / (total_duration_ns / 1e9)), 1) if total_duration_ns > 0 else 0.0
                return reply, tps
        except Exception as e:
            return f"[Device Manager Local Error]: Could not query Ollama engine ({str(e)}). Ensure Ollama is active locally.", 0.0

        return "[Device Manager Error]: Failed to generate response.", 0.0

qwen_engine = QwenEngine()
