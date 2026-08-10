@echo off
cd /d "C:\Users\sasi vardhan.P\myname\device_manager"
start /b "" "C:\Users\sasi vardhan.P\anaconda3\python.exe" -m uvicorn server:app --host 127.0.0.1 --port 8088
timeout /t 3 /nobreak >nul
start /b "" "C:\Users\sasi vardhan.P\anaconda3\python.exe" spidy_listener.py
start "" "http://127.0.0.1:8088"
