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

REM Ask if user wants to create desktop shortcut
set /p create_shortcut="Do you want to create a desktop shortcut? (Y/N): "
if /i "%create_shortcut%"=="Y" (
    echo.
    echo Creating desktop shortcut...
    echo.

    REM Get the current directory
    set APP_DIR=%~dp0
    set APP_DIR=%APP_DIR:~0,-1%
    set DESKTOP=%USERPROFILE%\Desktop

    REM Create VBScript to generate shortcut
    echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
    echo sLinkFile = "%DESKTOP%\Learning Tracker.lnk" >> CreateShortcut.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
    echo oLink.TargetPath = "%APP_DIR%\run_windows.bat" >> CreateShortcut.vbs
    echo oLink.WorkingDirectory = "%APP_DIR%" >> CreateShortcut.vbs
    echo oLink.Description = "Track your learning progress" >> CreateShortcut.vbs
    echo oLink.IconLocation = "C:\Windows\System32\imageres.dll,98" >> CreateShortcut.vbs
    echo oLink.Save >> CreateShortcut.vbs

    cscript //nologo CreateShortcut.vbs
    del CreateShortcut.vbs

    echo Desktop shortcut created!
    echo.
)

REM Ask if user wants to run the app now
set /p run_now="Do you want to run the application now? (Y/N): "
if /i "%run_now%"=="Y" (
    echo.
    echo Starting Learning Tracker...
    python main.py
) else (
    echo.
    echo You can run the application later:
    echo   - Double-click 'run_windows.bat'
    echo   - Or use the desktop shortcut (if created)
)

echo.
pause
