' Learning Tracker - Desktop Shortcut Creator (VBScript)
' Alternative shortcut creator for systems where batch files don't work well

Set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the script's directory (where the app is)
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Get desktop path
desktopPath = WshShell.SpecialFolders("Desktop")

' Create the shortcut
shortcutPath = desktopPath & "\Learning Tracker.lnk"
Set shortcut = WshShell.CreateShortcut(shortcutPath)

shortcut.TargetPath = scriptDir & "\run_windows.bat"
shortcut.WorkingDirectory = scriptDir
shortcut.Description = "Track your learning progress with PDF monitoring and Anki flashcards"
shortcut.IconLocation = "C:\Windows\System32\imageres.dll,98"

shortcut.Save

' Show success message
MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & _
       "A shortcut named 'Learning Tracker' has been" & vbCrLf & _
       "created on your desktop.", vbInformation, "Learning Tracker"
