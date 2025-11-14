# Automatic Updates Guide

Learning Tracker includes a built-in automatic update system that checks GitHub for new releases and installs them with one click.

## How It Works

The auto-update system:
1. **Checks GitHub** for the latest release
2. **Compares versions** to see if an update is available
3. **Downloads** the update ZIP file
4. **Installs** it automatically while preserving your data
5. **Restarts** the app with the new version

## Features

### ✅ Automatic Update Checks
- Checks for updates on app startup (if enabled)
- Checks once per day by default
- Can be disabled in Settings

### 📦 One-Click Installation
- Download and install with a single click
- Progress bar shows installation status
- Preserves your data and settings

### 🔒 Safe Updates
- **Data protection**: Your `data/` folder (database, settings) is never overwritten
- **Export protection**: Your `exports/` folder is preserved
- **Backup system**: Creates temporary backups during installation
- **Rollback-friendly**: Just reinstall the old version if needed

### 🎯 Smart Version Checking
- Only notifies when newer versions are available
- Compares semantic versions (e.g., 2.1.0 > 2.0.0)
- Shows release notes before installing

## Using Auto-Update

### Check for Updates Manually

1. Open Learning Tracker
2. Go to **⚙️ Settings** tab
3. Find the **🔄 Automatic Updates** section
4. Click **🔍 Check for Updates**

If an update is available:
- You'll see the version number and release notes
- Click **Yes** to install
- The app will download, install, and restart automatically

### Enable/Disable Automatic Checks

In the Settings tab, under Automatic Updates:
- ✅ **Check automatically on startup** - Enable/disable auto-checks
- When enabled: Checks once per day on startup
- When disabled: Only checks when you click the button

### Update Notification on Startup

When auto-check is enabled and an update is found:
1. A popup appears showing the new version
2. You can choose to:
   - **View updates section** - Go to Settings to install
   - **Not now** - Dismiss and update later

## What Gets Updated

### ✅ Updated Files:
- All Python source code (`src/` folder)
- Scripts (`*.bat`, `*.vbs` files)
- Documentation (`*.md` files)
- Configuration files
- The main application (`main.py`)

### 🔒 Protected Files (Never Overwritten):
- `data/` - Your database and settings
- `exports/` - Your exported Anki decks
- User-created files

## Installation Process

When you install an update:

1. **Download** (10-40%)
   - Downloads ZIP from GitHub
   - Shows progress

2. **Extract** (40-80%)
   - Extracts new files to temporary location
   - Validates contents

3. **Install** (80-95%)
   - Backs up your data
   - Replaces old files with new ones
   - Restores your data

4. **Finalize** (95-100%)
   - Cleans up temporary files
   - Verifies installation

5. **Restart**
   - App closes automatically
   - Restart it to use the new version

## Troubleshooting

### Update Check Fails

**Error: "Failed to check for updates"**

Possible causes:
- No internet connection
- GitHub is temporarily unavailable
- Firewall blocking the connection

**Solution:**
- Check your internet connection
- Try again later
- Click "Check for Updates" manually

### Update Installation Fails

**Error: "Update installation failed"**

Possible causes:
- Insufficient disk space
- File permissions issue
- Antivirus blocking installation

**Solution:**
1. Make sure you have at least 100MB free space
2. Run the app as Administrator (Windows)
3. Temporarily disable antivirus
4. Try installing again

### Update Doesn't Apply

**The app still shows the old version after update**

**Solution:**
1. Make sure you completely closed the app
2. Restart the app
3. Check Settings → About for the current version
4. If still old, manually download the new version

## Manual Update (Alternative)

If auto-update doesn't work, you can update manually:

### Windows:
```cmd
cd C:\Path\To\Quissapp
git pull origin main
pip install -r requirements.txt --upgrade
python main.py
```

### Or download fresh:
1. Download the latest ZIP from GitHub
2. Extract to a new folder
3. Copy your `data/` and `exports/` folders from the old installation
4. Run the new version

## Version Information

### Current Version Display
The Settings tab shows:
- **Current Version**: Your installed version (e.g., v2.0.0)
- **Update Status**: Check results and available updates

### Checking GitHub Releases

To see all available versions:
1. Visit: https://github.com/phorens/Quissapp/releases
2. View release notes and download options
3. Compare with your current version

## Update Settings

Settings are stored in `data/update_settings.json`:

```json
{
  "auto_check": true,
  "last_check": "2025-11-14T10:30:00",
  "check_interval_days": 1
}
```

**Configuration:**
- `auto_check`: Enable/disable automatic checking
- `last_check`: When the last check was performed
- `check_interval_days`: Days between checks (default: 1)

You can manually edit this file to change settings.

## Privacy & Security

### What Data Is Sent?
- **Version check**: Only your user agent string
- **No personal data** is transmitted
- **No usage tracking** or analytics

### Security Measures
- Downloads only from official GitHub repository
- Uses HTTPS for all connections
- Validates downloaded files before installation
- Creates backups before making changes

## Benefits of Auto-Update

✅ **Always up-to-date**: Get new features automatically
✅ **Bug fixes**: Security and stability improvements
✅ **Easy**: One-click installation
✅ **Safe**: Your data is never lost
✅ **Convenient**: No need to manually download
✅ **Informed**: See release notes before updating

## For Developers

### Creating Releases for Auto-Update

To make your updates available to users:

1. **Create a GitHub Release**:
   ```bash
   git tag v2.1.0
   git push origin v2.1.0
   ```

2. **On GitHub**:
   - Go to Releases → Create a new release
   - Tag: `v2.1.0`
   - Title: `Learning Tracker v2.1.0`
   - Add release notes
   - Optionally attach ZIP file (or use auto-generated source code)

3. **Users will be notified**:
   - Next time they start the app
   - Or when they click "Check for Updates"

### Version Numbering

Use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes only

Example: `2.1.3`
- Major: 2
- Minor: 1
- Patch: 3

## FAQ

**Q: How often does it check for updates?**
A: Once per day when you start the app (if enabled).

**Q: Can I disable auto-update?**
A: Yes, uncheck "Check automatically on startup" in Settings.

**Q: Will it update without asking?**
A: No, it always asks permission before installing.

**Q: What if I'm offline?**
A: Update checks will fail silently. Try again when online.

**Q: Can I rollback an update?**
A: Download and install the previous version manually.

**Q: Does it work with winget?**
A: Auto-update is independent of winget. Both can be used.

**Q: Will my data be lost?**
A: No, your database, exports, and settings are always preserved.

---

**Need help?** Check the main [README.md](README.md) or open an issue on GitHub.
