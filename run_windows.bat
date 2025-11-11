@echo off
REM Learning Tracker - Windows Run Script
REM Double-click this file to run the Learning Tracker application

echo Starting Learning Tracker...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please run setup_windows.bat first
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import genanki" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Dependencies not installed
    echo.
    echo Please run setup_windows.bat first to install dependencies
    echo.
    pause
    exit /b 1
)

REM Create directories if they don't exist
if not exist "data" mkdir data
if not exist "exports" mkdir exports

REM Run the application
python main.py

REM If the app exits with an error, show the error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
