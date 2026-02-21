@echo off
REM Sit-Too-Long - Quick Startup Script
REM Function: Auto-install dependencies if not installed, then start program

color 07
cls

echo.
echo ================================
echo Sit-Too-Long - Quick Startup
echo ================================
echo.

REM Get script directory
setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"

REM Check virtual environment
if not exist "%SCRIPT_DIR%venv" (
    echo [INFO] Virtual environment not detected
    echo.
    echo Running auto-installation...
    echo.
    powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install.ps1"
    if errorlevel 1 (
        echo.
        echo [ERROR] Auto-installation failed!
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call "%SCRIPT_DIR%venv\Scripts\activate.bat"

REM Run program
echo.
echo [INFO] Starting program...
echo.
python "%SCRIPT_DIR%sit-too-long.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Execution failed!
    pause
    exit /b 1
)

pause