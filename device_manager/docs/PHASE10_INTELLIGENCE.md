# 🕷️ SPIDY AI — PHASE 10: JARVIS NATURAL INTELLIGENCE & CONTEXT AWARENESS

## 1. Overview
Phase 10 transforms Spidy AI from a command-driven voice assistant into a fully conversational, context-aware, JARVIS-style personal computer companion. 

Users can speak naturally (*"Can you launch Google Chrome?"*, *"Turn the volume up"*, *"Make it louder"*, *"What app am I using?"*, *"Open Chrome and Notepad"*, *"Who created it?"*) without memorizing rigid synthetic commands.

---

## 2. Key Architecture Components

### 2.1 Conversational Context & Reference Engine (`core/conversation_context.py`)
- **Rolling Context Window:** Keeps a memory-bounded 10-turn conversation history.
- **Pronoun Resolution (`resolve_references`):**
  - Application pronouns: *"Open Chrome."* ➔ *"Close it."* ➔ Resolves `"it"` to `"Google Chrome"`.
  - Folder pronouns: *"Open Downloads."* ➔ *"Open that folder."* ➔ Resolves `"that folder"` to `"Downloads"`.
  - AI Subject pronouns: *"What is Python?"* ➔ *"Who created it?"* ➔ Resolves `"it"` to `"Python"`.

### 2.2 Active Window Context (`system/window_context.py`)
- Uses Windows Win32 API (`win32gui.GetForegroundWindow()`) to dynamically detect focused window titles and active process names.
- Maps complex executable names to friendly app aliases (*"VS Code"*, *"Google Chrome"*, *"Notepad"*, *"Calculator"*, *"File Explorer"*).
- Acts as a fallback for application actions when no explicit app is referenced in conversational turn history.

### 2.3 JARVIS Personality Formatter (`core/jarvis_personality.py`)
- Replaces generic, robotic text (*"COMMAND EXECUTED"*) with calm, concise, professional JARVIS responses:
  - *"Opening Google Chrome, boss."*
  - *"Closed Google Chrome, boss."*
  - *"Volume increased, boss."*
  - *"At your service, boss."*
- Uses `"boss"` naturally without repetitive boilerplate on every single sentence.

### 2.4 Multi-Step Natural Request Splitter (`core/intent_router.py` & `actions/executor.py`)
- Splits compound requests (*"Open Chrome and Notepad"*, *"Increase volume then open Downloads"*) into structured multi-action plans.
- Executes actions sequentially via `CapabilityRegistry` while reporting real-time step status via `EventBus`.

### 2.5 Strict Control Flow Routing Priority
1. **Wake Word** (Immediate SAPI5 greeting, 0 Qwen calls)
2. **Fast Deterministic Commands** (0ms latency, 0 Qwen calls for volume, application control, system locks)
3. **Existing OS Capabilities** (`AppManager`, `FileManager`, `SystemManager`)
4. **Conversational Context & Pronoun Resolution**
5. **Multi-Step Action Planner**
6. **Local FAISS RAG Search** (Instant offline vector lookup)
7. **Local Qwen3 1.7B LLM** (Fallback for general knowledge and open-ended queries)

---

## 3. Verified Test Suite Results

| Test Category | Command / Scenario | Result | Latency / Call Count |
|---|---|---|---|
| Natural App Launch | `"Can you open Chrome?"` | PASS | 337ms (Deterministic) |
| Natural Volume Control | `"Turn the volume up"`, `"Make it louder"` | PASS | < 1ms (Deterministic) |
| Pronoun Resolution | `"Open Chrome"` ➔ `"Close it"` | PASS | 1518ms (App Closed) |
| Folder Pronoun | `"Open Downloads"` ➔ `"Open that folder"` | PASS | 19ms (Folder Opened) |
| AI Topic Reference | `"What is Python?"` ➔ `"Who created it?"` | PASS | Topic Resolved |
| Active Window Query | `"What application am I using?"` | PASS | Win32 API Verified |
| Multi-Step Planning | `"Open Chrome and Notepad"` | PASS | 2-step Execution |
| Local Memory | `"Remember that my project is in Downloads"` | PASS | Saved in SQLite |
| Security Policy | `"run powershell -c Remove-Item C:\*"` | PASS | Blocked (0 Shell Execution) |
| Zero-Qwen Guarantee | `"open calculator"`, `"increase volume"` | PASS | **0 Qwen Calls** |

---

## 4. Operational Instructions
Start Spidy AI with Phase 10 Jarvis Intelligence using the unified startup batch:
```cmd
start_spidy.bat
```
Verify system status at:
```http
http://127.0.0.1:8088/health
```
