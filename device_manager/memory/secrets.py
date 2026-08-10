import re
from memory.config import SECRET_PATTERNS, MEMORY_SECRET_DETECTION

def is_secret(text: str) -> bool:
    if not MEMORY_SECRET_DETECTION or not text:
        return False

    clean_text = text.strip()
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, clean_text, re.IGNORECASE):
            return True
    return False
