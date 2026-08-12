# 🔒 SPIDY AI — VOICE IDENTITY & SPEAKER VERIFICATION MODEL

## 1. Overview
Spidy AI features an offline, local CPU speaker verification layer to ensure commands are executed exclusively when spoken by the authorized user.

---

## 2. Enrollment Procedure
To enroll your voice profile, open CMD in the project root and run:
```cmd
python -m voice.enroll
```
The utility will prompt you to repeat the phrase *"Hey Spidy, activate my assistant"* 5 times to generate your local embedding stored at:
```
data/voice_profile/speaker_embedding.npy
```
- **Privacy Model:** No raw audio recordings or embeddings leave your computer.
- **Offline operation:** Runs 100% locally without cloud API calls.

---

## 3. Runtime Verification Flow

```
Microphone Audio
       ↓
Wake Word Detection ("Hey Spidy")
       ↓
Speaker Verification Engine (Cosine Similarity)
       ↓
Is Authorized Speaker?
    ├── YES ➔ Process Command ➔ Execute Action ➔ SAPI5 TTS Response
    └── NO  ➔ Log Security Audit in Terminal ➔ Silent Rejection (0 Action / 0 TTS)
```

---

## 4. Multi-Layered Security Policy
Speaker verification serves as an entry authentication layer. All actions remain governed by Spidy AI's core security pipeline:
`VOICE IDENTITY` ➔ `WAKE WORD` ➔ `INTENT VALIDATION` ➔ `ACTION VALIDATION` ➔ `RISK CLASSIFICATION` ➔ `EXECUTION`

Arbitrary shell execution (`cmd.exe`, `PowerShell`, `shell=True`) remains strictly prohibited regardless of speaker authentication.
