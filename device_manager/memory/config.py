import os

# Memory Settings
MEMORY_ENABLED = True
MAX_MEMORIES = 200
MAX_MEMORY_VALUE_LENGTH = 300
MAX_SESSION_MESSAGES = 10
MAX_CONTEXT_TOKENS = 1500
MEMORY_CONFIDENCE_THRESHOLD = 0.6
SESSION_SUMMARY_ENABLED = True
MEMORY_SECRET_DETECTION = True

# Secret Detection Regex Patterns
SECRET_PATTERNS = [
    r"\b(sk-[a-zA-Z0-9_\-]{20,})\b",            # OpenAI / LLM Keys
    r"\b(ghp_[a-zA-Z0-9]{36})\b",               # GitHub PAT
    r"\b(AKIA[0-9A-Z]{16})\b",                  # AWS Access Key
    r"\b([a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27})\b", # Discord Token
    r"\b(bearer\s+[a-zA-Z0-9\._\-]+)\b",        # Bearer Tokens
    r"\b(BEGIN\s+(RSA|EC|DSA|OPENSSH)\s+PRIVATE\s+KEY)\b", # Private Keys
    r"\b(password|passwd|secret|api_key|apikey|auth_token)\s*[:=]\s*\S+\b" # Generic Key-Value Secrets
]
