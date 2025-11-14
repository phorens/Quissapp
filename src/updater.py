"""Auto-update system for Learning Tracker"""

import os
import sys
import json
import zipfile
import shutil
import tempfile
from typing import Optional, Tuple
from datetime import datetime, timedelta
try:
    import urllib.request
    import urllib.error
    URLLIB_AVAILABLE = True
except ImportError:
    URLLIB_AVAILABLE = False


class UpdateChecker:
    """Checks for and installs app updates from GitHub"""

    def __init__(self, current_version: str = "2.0.0",
                 repo_owner: str = "phorens",
                 repo_name: str = "Quissapp"):
        """Initialize update checker

        Args:
            current_version: Current app version
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name
        """
        self.current_version = current_version
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.settings_file = "data/update_settings.json"

    def get_update_settings(self) -> dict:
        """Load update settings

        Returns:
            Dictionary with update settings
        """
        default_settings = {
            "auto_check": True,
            "last_check": None,
            "check_interval_days": 1
        }

        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
        except:
            pass

        return default_settings

    def save_update_settings(self, settings: dict):
        """Save update settings

        Args:
            settings: Dictionary with update settings
        """
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except:
            pass

    def should_check_for_updates(self) -> bool:
        """Check if it's time to check for updates

        Returns:
            True if should check, False otherwise
        """
        settings = self.get_update_settings()

        if not settings.get("auto_check", True):
            return False

        last_check = settings.get("last_check")
        if not last_check:
            return True

        try:
            last_check_date = datetime.fromisoformat(last_check)
            interval_days = settings.get("check_interval_days", 1)
            next_check = last_check_date + timedelta(days=interval_days)

            return datetime.now() >= next_check
        except:
            return True

    def check_for_updates(self) -> Optional[dict]:
        """Check GitHub for latest release

        Returns:
            Dictionary with update info if available, None if no update or error
            {
                'version': '2.1.0',
                'download_url': 'https://...',
                'release_notes': 'What's new...',
                'published_at': '2025-11-14T...'
            }
        """
        if not URLLIB_AVAILABLE:
            return None

        try:
            # Update last check time
            settings = self.get_update_settings()
            settings["last_check"] = datetime.now().isoformat()
            self.save_update_settings(settings)

            # Fetch latest release info
            req = urllib.request.Request(self.github_api_url)
            req.add_header('User-Agent', 'LearningTracker-UpdateChecker')

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            latest_version = data.get('tag_name', '').lstrip('v')

            # Compare versions
            if self._is_newer_version(latest_version, self.current_version):
                # Find the ZIP asset
                download_url = None
                for asset in data.get('assets', []):
                    if asset.get('name', '').endswith('.zip'):
                        download_url = asset.get('browser_download_url')
                        break

                # If no asset, use the source code ZIP
                if not download_url:
                    download_url = data.get('zipball_url')

                return {
                    'version': latest_version,
                    'download_url': download_url,
                    'release_notes': data.get('body', 'No release notes available'),
                    'published_at': data.get('published_at', '')
                }

            return None

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # No releases yet
                return None
            raise
        except Exception as e:
            print(f"Update check failed: {e}")
            return None

    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compare version strings

        Args:
            latest: Latest version string (e.g., "2.1.0")
            current: Current version string (e.g., "2.0.0")

        Returns:
            True if latest is newer than current
        """
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]

            # Pad with zeros if needed
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)

            return latest_parts > current_parts
        except:
            return False

    def download_and_install_update(self, download_url: str,
                                    progress_callback=None) -> Tuple[bool, str]:
        """Download and install update

        Args:
            download_url: URL to download update ZIP
            progress_callback: Optional callback(percentage) for progress updates

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not URLLIB_AVAILABLE:
            return False, "Update system not available"

        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "update.zip")

            # Download update
            if progress_callback:
                progress_callback(10)

            urllib.request.urlretrieve(download_url, zip_path)

            if progress_callback:
                progress_callback(40)

            # Extract update
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            if progress_callback:
                progress_callback(60)

            # Find the actual app directory in extracted files
            app_dir = extract_dir
            # GitHub zipballs extract to a folder like "owner-repo-commitid"
            subdirs = [d for d in os.listdir(extract_dir)
                      if os.path.isdir(os.path.join(extract_dir, d))]
            if subdirs:
                app_dir = os.path.join(extract_dir, subdirs[0])

            # Get current app directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            if progress_callback:
                progress_callback(70)

            # Backup critical files
            backup_files = ['data', 'exports']
            backup_dir = os.path.join(temp_dir, "backup")
            os.makedirs(backup_dir, exist_ok=True)

            for item in backup_files:
                src = os.path.join(current_dir, item)
                if os.path.exists(src):
                    dst = os.path.join(backup_dir, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)

            if progress_callback:
                progress_callback(80)

            # Copy new files (excluding data and exports)
            for item in os.listdir(app_dir):
                if item in ['data', 'exports', '__pycache__', '.git']:
                    continue

                src = os.path.join(app_dir, item)
                dst = os.path.join(current_dir, item)

                # Remove old file/directory
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)

                # Copy new file/directory
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            if progress_callback:
                progress_callback(95)

            # Restore backup files
            for item in backup_files:
                src = os.path.join(backup_dir, item)
                dst = os.path.join(current_dir, item)
                if os.path.exists(src):
                    if os.path.isdir(src) and os.path.exists(dst):
                        # Merge directories
                        continue
                    elif os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)

            if progress_callback:
                progress_callback(100)

            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)

            return True, "Update installed successfully! Please restart the application."

        except Exception as e:
            return False, f"Update failed: {str(e)}"

    def get_current_version(self) -> str:
        """Get current app version

        Returns:
            Version string
        """
        return self.current_version
