# 🔒 SPIDY AI — ACTION SECURITY & PERMISSION MODEL

## Security Boundaries & Risk Model

Spidy AI enforces a strict multi-tier security model to prevent unauthorized system modifications, prompt injection attacks, or malicious RAG payload execution.

---

## 1. Risk Classification Tiers

| Risk Tier | Operations Included | Handling |
| :--- | :--- | :--- |
| **LOW** | `OPEN_APPLICATION` (allowed apps), `VOLUME_UP/DOWN`, `TYPE_TEXT` (<500 chars), `PRESS_KEY`, `HOTKEY`, `SWITCH_WINDOW` | Auto-executed after validation |
| **MEDIUM** | `CLOSE_APPLICATION`, `LOCK_SCREEN`, `OPEN_FOLDER`, `OPEN_FILE` | Logged and verified |
| **HIGH** | Potentially destructive OS operations | Requires explicit confirmation |
| **BLOCKED** | Shell execution (`rm -rf`, `powershell`, `cmd`), unapproved `.exe`, path traversal (`../`), credential theft | Immediately rejected |

---

## 2. Hard Security Restrictions
- **Zero Raw Shell Execution:** Neither Qwen3 nor the Action Engine can execute raw `cmd.exe`, `powershell.exe`, or `bash` scripts.
- **Trusted Application Allowlist:** Only pre-approved applications in `ALLOWED_APPLICATIONS` (e.g., `calculator`, `notepad`, `chrome`, `code`, `explorer`) are launchable.
- **RAG Execution Separation:** Information retrieved from local documents is treated as pure text data and cannot trigger action execution.
- **Path Traversal Protection:** All file paths containing `..` or relative directory jumps are rejected automatically.
