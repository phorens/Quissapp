# Setting Up Winget for Learning Tracker

This guide explains how to make Learning Tracker available through Windows Package Manager (winget).

## What is Winget?

Winget is Windows' official package manager, allowing users to install and update apps with simple commands like:
```powershell
winget install LearningTracker.LearningTracker
winget upgrade LearningTracker.LearningTracker
```

## Current Status

The winget manifest has been prepared in `.winget/manifest.yaml`. To make the app available through winget, you need to:

1. **Create GitHub Releases**
2. **Submit to Microsoft's winget repository**

## How to Enable Winget Distribution

### Step 1: Create a GitHub Release

1. **Create a ZIP archive** of the application:
   ```bash
   # On Windows, from the Quissapp directory:
   tar -a -c -f LearningTracker-v2.0.0.zip main.py src requirements.txt *.bat *.md .gitignore
   ```

2. **Create a release on GitHub**:
   - Go to your repository: https://github.com/phorens/Quissapp
   - Click "Releases" → "Create a new release"
   - Tag: `v2.0.0`
   - Title: `Learning Tracker v2.0.0`
   - Upload the `LearningTracker-v2.0.0.zip` file
   - Add release notes
   - Publish the release

3. **Get the SHA256 hash** of the ZIP file:
   ```powershell
   # On Windows PowerShell:
   Get-FileHash LearningTracker-v2.0.0.zip -Algorithm SHA256
   ```

4. **Update the manifest**:
   - Edit `.winget/manifest.yaml`
   - Replace `<TO_BE_GENERATED>` with the actual SHA256 hash
   - Update the `InstallerUrl` with the actual GitHub release URL

### Step 2: Submit to Winget Repository

1. **Fork the winget-pkgs repository**:
   - Go to: https://github.com/microsoft/winget-pkgs
   - Click "Fork"

2. **Create your package folder**:
   ```
   manifests/l/LearningTracker/LearningTracker/2.0.0/
   ```

3. **Split the manifest into required files**:

   Create `LearningTracker.LearningTracker.yaml`:
   ```yaml
   PackageIdentifier: LearningTracker.LearningTracker
   PackageVersion: 2.0.0
   DefaultLocale: en-US
   ManifestType: version
   ManifestVersion: 1.4.0
   ```

   Create `LearningTracker.LearningTracker.locale.en-US.yaml`:
   ```yaml
   PackageIdentifier: LearningTracker.LearningTracker
   PackageVersion: 2.0.0
   PackageLocale: en-US
   Publisher: LearningTracker
   PackageName: Learning Tracker
   License: MIT
   ShortDescription: Track your learning progress with PDF monitoring
   ManifestType: defaultLocale
   ManifestVersion: 1.4.0
   ```

   Create `LearningTracker.LearningTracker.installer.yaml`:
   ```yaml
   PackageIdentifier: LearningTracker.LearningTracker
   PackageVersion: 2.0.0
   Installers:
     - Architecture: x64
       InstallerType: zip
       InstallerUrl: https://github.com/phorens/Quissapp/releases/download/v2.0.0/LearningTracker-v2.0.0.zip
       InstallerSha256: <YOUR_SHA256_HERE>
   ManifestType: installer
   ManifestVersion: 1.4.0
   ```

4. **Create a Pull Request**:
   - Commit your changes to your fork
   - Create a PR to microsoft/winget-pkgs
   - Wait for review and approval

### Step 3: Testing Before Submission

Test your package locally:

```powershell
# Validate the manifest
winget validate --manifest path\to\manifest\folder

# Test installation locally
winget install --manifest path\to\manifest\folder
```

## Alternative: Manual Distribution

If you don't want to go through Microsoft's repository, users can still install via:

### Option 1: Direct Download
```powershell
# Download and extract
Invoke-WebRequest -Uri "https://github.com/phorens/Quissapp/archive/refs/heads/main.zip" -OutFile "LearningTracker.zip"
Expand-Archive LearningTracker.zip -DestinationPath C:\LearningTracker
cd C:\LearningTracker
pip install -r requirements.txt
python main.py
```

### Option 2: Git Clone
```powershell
git clone https://github.com/phorens/Quissapp.git
cd Quissapp
pip install -r requirements.txt
python main.py
```

## Automatic Updates

Once in winget, users can update with:
```powershell
winget upgrade LearningTracker.LearningTracker
```

To enable this:
1. Create new releases on GitHub for each version
2. Submit updated manifests to winget-pkgs

## Benefits of Winget Distribution

- ✅ Easy installation with one command
- ✅ Automatic updates
- ✅ Centralized package management
- ✅ Version control
- ✅ Trusted source (Microsoft repository)

## Notes

- Winget packages are reviewed by Microsoft before approval
- The review process typically takes 1-3 days
- You'll need to maintain the package with updates
- Consider creating an installer (MSI or EXE) for better integration

## Resources

- [Winget Documentation](https://docs.microsoft.com/en-us/windows/package-manager/)
- [Package Manifest Schema](https://docs.microsoft.com/en-us/windows/package-manager/package/manifest)
- [Submitting Packages](https://github.com/microsoft/winget-pkgs/blob/master/AUTHORING_MANIFESTS.md)
