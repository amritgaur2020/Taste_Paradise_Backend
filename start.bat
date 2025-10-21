@echo off
echo Starting TasteParadise Restaurant Management System...
echo.

REM Start React in new window
start "React Dev Server" cmd /k "cd frontend && npm start"

REM Wait 5 seconds for React to start
timeout /t 5 /nobreak > nul

REM Start FastAPI
echo Starting FastAPI Backend...
python main.py

REM When Python exits, kill React window
taskkill /FI "WindowTitle eq React Dev Server*" /F > nul 2>&1
