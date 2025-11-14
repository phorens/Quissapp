# Creating the v2.0.0 Release

I've created a local tag for v2.0.0. Now you need to create the GitHub Release manually to enable the update system.

## Steps to Create the Release

### 1. Go to GitHub Releases
Open this URL in your browser:
```
https://github.com/phorens/Quissapp/releases/new
```

### 2. Fill in the Release Form

**Choose a tag:** Create new tag on publish
- Tag: `v2.0.0`
- Target: `claude/learning-tracker-app-011CV2QaM8juaiEpCGWWMt7m` (or `main` if merged)

**Release title:**
```
Learning Tracker v2.0.0 - Initial Release
```

**Description (Release Notes):**
```markdown
# Learning Tracker v2.0.0 🎉

The first official release of Learning Tracker - a desktop app to track your daily learning progress!

## ✨ Features

### PDF Tracking
- 🔍 **Automatic PDF detection** - Monitor a folder and automatically track PDFs when opened
- ✋ **Manual tracking** - Start/stop tracking for any PDF file
- 📊 Daily statistics and session history
- 📄 Breakdown of time spent on each PDF
- 💾 Persistent monitoring settings (remembers your folder)

### Flashcard Management
- ✨ Create flashcards with question/answer format
- 📤 Export directly to Anki format (.apkg)
- 📄 Alternative CSV export
- ✅ Track which cards have been exported

### Daily Reminders
- 🔔 Automatic reminders at 9:00 AM, 2:00 PM, and 8:00 PM
- 🔔 System notifications to check your progress
- ✅ Mark daily check-ins to track consistency

### Automatic Updates
- 🔄 **One-click updates** - Download and install updates from within the app
- 🚀 Auto-check on startup (optional)
- 🔒 Safe installation - Your data is never overwritten
- 📊 Progress tracking during installation

### Modern UI
- 🎨 Professional blue and white theme
- 📇 Card-based layout
- 🎯 Clear visual indicators
- 📱 Responsive design

### Windows Integration
- 🖥️ Desktop shortcut creation
- 📦 Easy setup with batch scripts
- 🪟 Native Windows experience

## 📦 Installation

### Windows

1. **Download and extract** this release
2. **Install Python** 3.8+ from [python.org](https://www.python.org/downloads/)
   - ✓ Check "Add Python to PATH"
3. **Double-click `setup_windows.bat`** to install dependencies
4. **Double-click `run_windows.bat`** to launch

**Detailed guide:** See `INSTALL_WINDOWS.md`

### Linux/Mac

```bash
pip install -r requirements.txt
python main.py
```

## 📚 Quick Start

1. **Track PDFs**
   - Go to "PDF Tracking" tab
   - Click "Select Folder to Monitor" for automatic tracking
   - Or click "Start Tracking" to manually select a PDF

2. **Create Flashcards**
   - Go to "Flashcards" tab
   - Enter question and answer
   - Click "Export to Anki" when ready

3. **View Stats**
   - Check "Statistics" tab for your learning overview

## 🔧 System Requirements

- Python 3.8 or higher
- Windows 10/11, Linux, or macOS
- 100 MB disk space
- Internet connection (for updates)

## 🐛 Known Issues

None currently - this is the initial stable release!

## 📖 Documentation

- `README.md` - Main documentation
- `INSTALL_WINDOWS.md` - Windows installation guide
- `AUTO_UPDATE_GUIDE.md` - How to use automatic updates
- `CHANGELOG.md` - Version history

## 🙏 Feedback

Found a bug or have a feature request? Please open an issue!

---

**Version:** 2.0.0
**Release Date:** November 14, 2025
**Full Changelog:** See `CHANGELOG.md`
```

### 3. Publish the Release

- Check **"Set as the latest release"**
- Click **"Publish release"**

### 4. Test the Update System

Once published:

1. Open Learning Tracker
2. Go to Settings → Automatic Updates
3. Click "Check for Updates"
4. Should show: "✅ You're running the latest version!"

Since you're already on v2.0.0, it won't offer an update. But the system is now ready for future updates!

## For Future Releases

When you want to release v2.1.0:

```bash
# 1. Make your changes and commit
git add .
git commit -m "Add new features"
git push

# 2. Create tag
git tag v2.1.0
# Note: You'll need to create the tag via GitHub releases

# 3. Create release on GitHub (like above)
# Users will be notified and can update with one click!
```

## Alternative: Quick Release via GitHub UI

If tag pushing doesn't work, you can create everything through GitHub:

1. Go to: https://github.com/phorens/Quissapp/releases/new
2. Click "Choose a tag" → Type `v2.0.0` → "Create new tag on publish"
3. Fill in title and description (see above)
4. Click "Publish release"

That's it! The tag will be created automatically when you publish.
