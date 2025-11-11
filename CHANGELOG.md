# Changelog

All notable changes to Learning Tracker will be documented in this file.

## [2.0.0] - 2025-11-11

### ✨ New Features

#### Automatic PDF Detection
- **Auto-monitoring**: Select a folder to automatically track PDFs when opened
- **Persistent settings**: App remembers your monitored folder across sessions
- **Smart detection**: Debounced file events prevent duplicate tracking
- **Status indicators**: Clear visual feedback showing monitoring status

#### Enhanced User Interface
- **Modern design**: Complete UI overhaul with card-based layout
- **Color scheme**: Professional blue and white theme with accent colors
- **Emoji icons**: Visual indicators for better navigation
- **Better spacing**: Improved padding and layout for readability
- **Responsive design**: Better use of screen space
- **Custom styles**: Themed buttons, tabs, and components

#### Desktop Integration
- **Desktop shortcut**: Easy-to-use scripts for creating desktop shortcuts
- **Windows integration**: Proper icon and description for shortcuts
- **Quick launch**: Double-click shortcut to open app

#### Winget Support (Planned)
- **Package manifest**: Ready for Windows Package Manager submission
- **Auto-updates**: Framework for automatic updates via winget
- **Documentation**: Complete guide for winget setup and distribution

### 🔧 Improvements

#### PDF Tracking
- Both automatic and manual tracking now work seamlessly together
- Better session management with proper cleanup
- Improved time tracking accuracy
- Visual feedback for active tracking sessions

#### UI/UX
- Larger, more readable fonts (Segoe UI)
- Better contrast and color accessibility
- Clearer section headers and organization
- Improved button states and interactions
- More informative status messages

#### Documentation
- Comprehensive Windows installation guide
- Desktop shortcut creation instructions
- Winget setup documentation
- Updated README with new features

### 🐛 Bug Fixes
- Fixed PDF tracking initialization issues
- Improved error handling for directory monitoring
- Better cleanup on application exit
- Fixed monitor settings persistence

### 📁 File Structure Changes
```
New files:
- create_shortcut.bat        # Desktop shortcut creator
- create_shortcut.vbs        # Alternative shortcut creator
- WINGET_SETUP.md           # Winget distribution guide
- .winget/manifest.yaml     # Winget package manifest
- CHANGELOG.md              # This file

Modified files:
- src/gui.py                # Complete UI redesign
- setup_windows.bat         # Added shortcut creation
- INSTALL_WINDOWS.md        # Added shortcut instructions
- README.md                 # Updated with new features
```

## [1.0.0] - 2025-11-11

### Initial Release

#### Core Features
- PDF tracking with manual start/stop
- Flashcard creation and management
- Anki export (.apkg format)
- CSV export option
- Daily reminders (9 AM, 2 PM, 8 PM)
- Statistics dashboard
- SQLite database for data storage
- Windows batch scripts for installation
- Basic Tkinter GUI

#### Modules
- `database.py` - SQLite database operations
- `pdf_tracker.py` - PDF monitoring and tracking
- `flashcard_manager.py` - Flashcard management and Anki export
- `reminder_system.py` - Daily reminder notifications
- `gui.py` - Tkinter user interface

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **Major version** (X.0.0): Breaking changes or major features
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes and minor improvements
