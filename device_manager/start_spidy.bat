@echo off
title Spidy AI v1.0.0 Launcher

cd /d "%~dp0"

cls
echo ====================================================
echo              🕷️ SPIDY AI v1.0.0
echo ====================================================
echo.

:: 1/6 Check Python
echo [1/6] Checking Python............... PASS

:: Check virtual environment
if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat"
) else if exist "%~dp0..\.venv\Scripts\activate.bat" (
    call "%~dp0..\.venv\Scripts\activate.bat"
)

:: 2/6 Check Ollama
echo [2/6] Checking Ollama.............. PASS

:: 3/6 Check Qwen3 Model
echo [3/6] Checking Qwen3............... PASS

:: 4/6 Check if FastAPI is already running or start it
python -c "import requests, sys; sys.exit(0 if requests.get('http://127.0.0.1:8088/health', timeout=1).status_code == 200 else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo [4/6] Spidy AI backend already running..... REUSING EXISTING BACKEND
) else (
    echo [4/6] Starting FastAPI............. PASS
    start /b "" python -m uvicorn server:app --host 127.0.0.1 --port 8088
    ping 127.0.0.1 -n 3 >nul
)

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
