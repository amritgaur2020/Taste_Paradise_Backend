@echo off
echo Starting with full error capture...
echo.

python -c "import subprocess; subprocess.run(['TasteParadise.exe'], capture_output=False)" 2>&1

echo.
echo ===== OR try this: =====
echo.

start /wait TasteParadise.exe

pause
