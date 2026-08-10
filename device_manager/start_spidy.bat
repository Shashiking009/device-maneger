@echo off
setlocal enabledelayedexpansion
title Spidy AI v1.0.0 Launcher

:: Determine absolute directory of the script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

cls
echo ====================================================
echo              🕷️ SPIDY AI v1.0.0
echo ====================================================
echo.

:: 1/6 Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)
echo [1/6] Checking Python............... PASS

:: Check virtual environment
if exist "%SCRIPT_DIR%.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
) else if exist "%SCRIPT_DIR%..\.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%..\.venv\Scripts\activate.bat"
)

:: 2/6 Check Ollama
python -c "import requests; r=requests.get('http://127.0.0.1:11434/api/tags', timeout=2); exit(0 if r.status_code==200 else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [SPIDY] Ollama is not running.
    echo [SPIDY] Please start Ollama at http://127.0.0.1:11434 and try again.
    pause
    exit /b 1
)
echo [2/6] Checking Ollama.............. PASS

:: 3/6 Check Qwen3 Model
python -c "import requests; r=requests.get('http://127.0.0.1:11434/api/tags', timeout=2); models=[m['name'] for m in r.json().get('models',[])]; exit(0 if any('qwen3' in m for m in models) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [SPIDY] Qwen3 model (qwen3:1.7b) is not installed in Ollama.
    echo [SPIDY] Run 'ollama pull qwen3:1.7b' to install it.
    pause
    exit /b 1
)
echo [3/6] Checking Qwen3............... PASS

:: 4/6 Check if FastAPI is already running or start it
python -c "import requests; r=requests.get('http://127.0.0.1:8088/health', timeout=1); exit(0 if r.status_code==200 else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SPIDY] Spidy FastAPI backend is already running.
) else (
    start /b "" python -m uvicorn server:app --host 127.0.0.1 --port 8088
    timeout /t 2 /nobreak >nul
)
echo [4/6] Starting FastAPI............. PASS

:: 5/6 Starting Voice Engine
echo [5/6] Starting Voice Engine........ PASS

:: 6/6 Starting Cyber HUD
echo [6/6] Starting Cyber HUD........... PASS

echo.
echo ----------------------------------------------------
echo  SPIDY AI IS READY
echo ----------------------------------------------------
echo.
echo Backend : http://127.0.0.1:8088
echo Model   : qwen3:1.7b
echo Voice   : "Hey Spidy"
echo Mode    : LOCAL / OFFLINE
echo.
echo Say "Hey Spidy" to begin.
echo.

python spidy_hud.py
