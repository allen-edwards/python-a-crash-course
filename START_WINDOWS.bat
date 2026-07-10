@echo off
title Python: A Crash Course — A Beginner's Journey
echo.
echo  =====================================================
echo   Python: A Crash Course — A Beginner's Journey
echo  =====================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python not found!
    echo.
    echo  Install Python 3 from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo  Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo  Installing Flask (one-time setup)...
    pip install flask --quiet
)

REM Create Desktop shortcut (Windows)
set APP_DIR=%~dp0
set SHORTCUT=%USERPROFILE%\Desktop\Python A Crash Course.bat
if not exist "%SHORTCUT%" (
    echo @echo off > "%SHORTCUT%"
    echo cd /d "%APP_DIR%" >> "%SHORTCUT%"
    echo call START_WINDOWS.bat >> "%SHORTCUT%"
    echo  Shortcut created on Desktop!
)

echo  Starting app — your browser will open automatically.
echo  Close this window to stop the app.
echo.
python app.py
pause
