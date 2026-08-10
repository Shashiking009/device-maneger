@echo off
cd /d "%~dp0"
start /b "" python -m uvicorn server:app --host 127.0.0.1 --port 8088
timeout /t 2 /nobreak >nul
start /b "" python spidy_hud.py
