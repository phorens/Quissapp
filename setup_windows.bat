@echo off
REM Learning Tracker - Windows Setup Script
REM This script will install dependencies and set up the application

echo ========================================
echo Learning Tracker - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check pip
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo.
    pause
    exit /b 1
)
echo pip is available
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo   1. Double-click 'run_windows.bat'
echo   2. Or open Command Prompt and run: python main.py
echo.
echo Creating data directory...
if not exist "data" mkdir data
if not exist "exports" mkdir exports
echo.

REM Ask if user wants to run the app now
set /p run_now="Do you want to run the application now? (Y/N): "
if /i "%run_now%"=="Y" (
    echo.
    echo Starting Learning Tracker...
    python main.py
) else (
    echo.
    echo You can run the application later using run_windows.bat
)

echo.
pause
