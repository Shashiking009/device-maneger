# 🖥️ SPIDY AI — TERMINAL CONVERSATION DISPLAY

## 1. Terminal Display Format
When running Spidy AI in Windows CMD, the conversation pipeline is printed in a clean, structured format:

```text
============================================================
[21:15:05] USER
> hey spidy open downloads

[21:15:05] WAKE
[OK] "hey spidy" detected

[21:15:05] VOICE AUTH
[OK] Authorized speaker
Confidence: 1.00

[21:15:05] COMMAND
> open downloads

[21:15:05] INTENT
> OPEN_FOLDER
Confidence: 1.00

[21:15:05] ACTION
> OPEN_FOLDER

[21:15:05] RESULT
[OK] SUCCESS
Details: Opening Downloads, boss.

[21:15:05] SPIDY
> Opening Downloads, boss.
============================================================
```

## 2. Security Filtering
The terminal logger automatically strips passwords, tokens, and sensitive system secrets from output.
