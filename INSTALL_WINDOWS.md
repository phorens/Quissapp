# Installing Learning Tracker on Windows

This guide will walk you through installing and running the Learning Tracker application on Windows.

## Prerequisites

### Step 1: Install Python

1. **Download Python:**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.8 or higher (recommend Python 3.11 or 3.12)
   - **Important:** Choose the Windows installer (64-bit recommended)

2. **Install Python:**
   - Run the downloaded installer
   - **✓ CHECK the box "Add Python to PATH"** (very important!)
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   - Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
   - Type: `python --version`
   - You should see something like: `Python 3.11.x`

### Step 2: Install Git (Optional - for cloning)

If you want to clone the repository:

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Restart Command Prompt after installation

## Installation Methods

### Method 1: Clone with Git (Recommended)

1. **Open Command Prompt** (Win + R → type `cmd` → Enter)

2. **Navigate to where you want to install:**
   ```cmd
   cd C:\Users\YourUsername\Documents
   ```

3. **Clone the repository:**
   ```cmd
   git clone http://127.0.0.1:20767/git/phorens/Quissapp
   cd Quissapp
   git checkout claude/learning-tracker-app-011CV2QaM8juaiEpCGWWMt7m
   ```

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```cmd
   python main.py
   ```

### Method 2: Download ZIP (Easier)

1. **Download the code:**
   - Download the repository as a ZIP file
   - Extract to a folder like `C:\Users\YourUsername\Documents\Quissapp`

2. **Open Command Prompt:**
   - Press `Win + R`
   - Type `cmd` and press Enter

3. **Navigate to the folder:**
   ```cmd
   cd C:\Users\YourUsername\Documents\Quissapp
   ```
   (Replace with your actual path)

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```cmd
   python main.py
   ```

## Quick Setup Script

You can also use the provided batch script for automatic setup:

1. Navigate to the Quissapp folder in File Explorer
2. Double-click `setup_windows.bat`
3. Follow the prompts
4. Choose whether to create a desktop shortcut
5. The application will launch automatically

### Creating a Desktop Shortcut

To create a desktop shortcut for easy access:

**Option 1:** During setup
- The setup script will ask if you want to create a shortcut

**Option 2:** Anytime after setup
- Double-click `create_shortcut.bat` in the Quissapp folder
- Or double-click `create_shortcut.vbs` for an alternative method

The shortcut will appear on your desktop as "Learning Tracker"

## Running the Application

### First Time Setup

When you first run the app:
```cmd
cd C:\Users\YourUsername\Documents\Quissapp
python main.py
```

The application will:
- Create a `data` folder for the database
- Create an `exports` folder for Anki exports
- Open the GUI window

### Daily Use

**Option 1: Command Line**
```cmd
cd C:\Users\YourUsername\Documents\Quissapp
python main.py
```

**Option 2: Double-click**
- Double-click `run_windows.bat` in the Quissapp folder

**Option 3: Create Desktop Shortcut**
1. Right-click `run_windows.bat`
2. Select "Send to" → "Desktop (create shortcut)"
3. Double-click the shortcut to launch

## Troubleshooting

### "Python is not recognized as a command"

**Solution:** Python is not in your PATH.

1. Search for "Environment Variables" in Windows Start menu
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Click "Edit"
5. Click "New" and add:
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts\`
   (Adjust version number as needed)
6. Click "OK" on all windows
7. **Restart Command Prompt**

### "pip is not recognized"

**Solution:** Try using `py -m pip` instead:
```cmd
py -m pip install -r requirements.txt
```

### "No module named tkinter"

**Solution:** Reinstall Python and make sure to check "tcl/tk and IDLE" during installation.

### Notifications Not Working

This is normal on Windows if you haven't granted notification permissions:
1. Go to Settings → System → Notifications
2. Allow notifications for Python or Command Prompt
3. The app works fine without notifications

### Permission Errors

**Solution:** Run Command Prompt as Administrator:
1. Search for "cmd" in Start menu
2. Right-click "Command Prompt"
3. Select "Run as administrator"

## Dependencies Explained

The app installs these packages:

- **genanki** - Creates Anki deck files (.apkg)
- **watchdog** - Monitors file system changes
- **plyer** - Sends system notifications
- **Pillow** - Image processing support

All are installed automatically with `pip install -r requirements.txt`

## Anki Integration

### Installing Anki

1. Download Anki from [apps.ankiweb.net](https://apps.ankiweb.net/)
2. Install Anki on your Windows machine
3. Open Anki at least once to set it up

### Importing Flashcards

1. In Learning Tracker, create flashcards and click "Export New Cards (.apkg)"
2. The file is saved to: `C:\Users\YourUsername\Documents\Quissapp\exports\`
3. Open Anki
4. Click "File" → "Import"
5. Navigate to the exports folder
6. Select the `.apkg` file
7. Your flashcards appear in the "Learning Tracker" deck

## Uninstallation

If you want to remove the application:

1. Delete the Quissapp folder
2. (Optional) Uninstall Python packages:
   ```cmd
   pip uninstall genanki watchdog plyer Pillow
   ```

Your learning data is stored only in the `data` folder inside Quissapp, so deleting the folder removes all data.

## Getting Help

If you encounter issues:

1. Make sure Python 3.8+ is installed and in PATH
2. Make sure all dependencies are installed
3. Check that you're in the correct directory
4. Try running as Administrator

## System Requirements

- **OS:** Windows 10 or Windows 11
- **Python:** 3.8 or higher
- **RAM:** 2 GB minimum
- **Disk Space:** 100 MB
- **Display:** 800x600 minimum resolution

---

**Happy Learning!** 📚

For more information, see the main README.md file.
