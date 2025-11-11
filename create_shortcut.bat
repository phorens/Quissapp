@echo off
REM Learning Tracker - Desktop Shortcut Creator
REM This script creates a desktop shortcut for the Learning Tracker app

echo ========================================
echo Learning Tracker - Shortcut Creator
echo ========================================
echo.

REM Get the current directory (where the app is installed)
set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%

REM Get the desktop path
set DESKTOP=%USERPROFILE%\Desktop

echo Creating desktop shortcut...
echo.
echo App location: %APP_DIR%
echo Desktop: %DESKTOP%
echo.

REM Create VBScript to generate shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\Learning Tracker.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%APP_DIR%\run_windows.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%APP_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Track your learning progress with PDF monitoring and Anki flashcards" >> CreateShortcut.vbs
echo oLink.IconLocation = "C:\Windows\System32\imageres.dll,98" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Run the VBScript
cscript //nologo CreateShortcut.vbs

REM Clean up
del CreateShortcut.vbs

echo.
echo ========================================
echo Shortcut created successfully!
echo ========================================
echo.
echo A shortcut named "Learning Tracker" has been
echo created on your desktop.
echo.
echo Double-click it to launch the app!
echo.
pause
