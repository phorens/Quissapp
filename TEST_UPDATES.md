# Testing the Update System

The update checker is working correctly, but it needs **at least one GitHub Release** to check against.

## Why "Check for Updates" Shows No Updates

The update system looks for releases on GitHub at:
```
https://api.github.com/repos/phorens/Quissapp/releases/latest
```

**If no releases exist**, it will show:
- ❌ "No releases found on GitHub repository"

## How to Test Updates

### Option 1: Create a Test Release (Recommended)

1. **Create a test version tag:**
   ```bash
   git tag v2.0.1-test
   git push origin v2.0.1-test
   ```

2. **Create a release on GitHub:**
   - Go to: https://github.com/phorens/Quissapp/releases
   - Click "Create a new release"
   - Choose tag: `v2.0.1-test`
   - Title: `Test Release v2.0.1`
   - Description: `Test release for update system`
   - Check "This is a pre-release" (so it's clearly marked as test)
   - Click "Publish release"

3. **Test the update checker:**
   - Open the app
   - Go to Settings → Automatic Updates
   - Click "Check for Updates"
   - Should show: "Update available: v2.0.1-test"

4. **Clean up:**
   ```bash
   git tag -d v2.0.1-test
   git push origin :refs/tags/v2.0.1-test
   ```
   - Delete the release on GitHub

### Option 2: Create a Real Release

When you're ready to release v2.1.0:

1. **Commit your final changes:**
   ```bash
   git add .
   git commit -m "Release v2.1.0"
   git push
   ```

2. **Create version tag:**
   ```bash
   git tag v2.1.0
   git push origin v2.1.0
   ```

3. **Create GitHub Release:**
   - Go to Releases → Create new release
   - Tag: `v2.1.0`
   - Title: `Learning Tracker v2.1.0`
   - Description: Release notes (what's new)
   - Publish release

4. **Users can now update:**
   - Click "Check for Updates"
   - See v2.1.0 available
   - Install with one click

## Current Status

**Current Version:** v2.0.0

**To test updates, you need to:**
1. Create a release with version > 2.0.0 (like v2.0.1 or v2.1.0)
2. The update system will detect it
3. Users can install it

## Testing Without GitHub Releases

If you want to test locally without creating releases, you can:

1. **Modify the version comparison:**
   In `src/updater.py`, temporarily change:
   ```python
   def __init__(self, current_version: str = "2.0.0",
   ```
   To:
   ```python
   def __init__(self, current_version: str = "1.0.0",  # Pretend we're on old version
   ```

2. **Create any release on GitHub** (even v2.0.0)

3. **Test** - The app will think it's on v1.0.0 and find v2.0.0 available

4. **Revert the change** when done testing

## Error Messages Explained

### "No releases found on GitHub repository"
- **Cause:** No releases exist on GitHub
- **Fix:** Create at least one release

### "GitHub API rate limit exceeded"
- **Cause:** Too many API requests (60/hour unauthenticated)
- **Fix:** Wait an hour or authenticate API requests

### "Network error: ..."
- **Cause:** No internet connection or firewall blocking
- **Fix:** Check internet connection

### "You're running the latest version"
- **Cause:** Current version (2.0.0) >= Latest release version
- **Fix:** Create a release with version > 2.0.0

## Quick Test Script

Create a test release quickly:

```bash
# Create test tag and release
git tag v2.0.1
git push origin v2.0.1

# Create release on GitHub (manual step)
# Then test the update checker in the app

# Clean up
git tag -d v2.0.1
git push origin :refs/tags/v2.0.1
# Delete release on GitHub
```

## Recommended Release Strategy

For real releases:
1. **v2.0.x** - Bug fixes and minor improvements
2. **v2.x.0** - New features
3. **v3.0.0** - Major changes or breaking updates

Always test with a pre-release first!
