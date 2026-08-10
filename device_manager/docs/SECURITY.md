# 🔒 SPIDY AI — SECURITY MODEL & BOUNDARIES

Spidy AI is engineered with defense-in-depth security principles to protect host operating systems from malicious prompts, unvalidated command execution, and credential leakage.

---

## Security Layers

1. **Local Network Binding:** FastAPI server binds exclusively to `127.0.0.1:8088`. It is not exposed to external LAN interfaces by default.
2. **Zero Raw Shell Access:** System does not permit raw `cmd.exe`, `powershell.exe`, or `bash` execution from user prompts, LLM responses, or RAG documents.
3. **Application Allowlist Enforcement:** `ActionValidator` verifies target application names against `ALLOWED_APPLICATIONS` (e.g. `calculator`, `notepad`, `chrome`, `code`, `explorer`). Unapproved `.exe` paths are rejected.
4. **Path Traversal Defense:** Rejects any file path containing relative directory jumps (`..`) or unauthorized file extensions.
5. **Secret Shield:** Secret detection regex scanner blocks storing API keys (`sk-`), GitHub PATs (`ghp_`), AWS keys (`AKIA`), Bearer tokens, or passwords in local memory.
