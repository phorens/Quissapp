"""PDF tracking module for monitoring PDF viewing time"""

import os
import time
from datetime import datetime
from threading import Thread, Event
from typing import Optional, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PDFTracker:
    """Tracks time spent viewing PDF files"""

    def __init__(self, database, update_callback: Optional[Callable] = None):
        """Initialize PDF tracker

        Args:
            database: Database instance for storing session data
            update_callback: Optional callback function called when tracking updates
        """
        self.database = database
        self.update_callback = update_callback
        self.current_session_id = None
        self.current_pdf_path = None
        self.current_pdf_name = None
        self.session_start_time = None
        self.is_tracking = False
        self.tracking_thread = None
        self.stop_event = Event()

    def start_tracking(self, pdf_path: str):
        """Start tracking a PDF viewing session

        Args:
            pdf_path: Full path to the PDF file being viewed
        """
        # End previous session if exists
        if self.is_tracking:
            self.stop_tracking()

        self.current_pdf_path = pdf_path
        self.current_pdf_name = os.path.basename(pdf_path)
        self.session_start_time = datetime.now()
        self.is_tracking = True

        # Create session in database
        self.current_session_id = self.database.add_pdf_session(
            pdf_path=self.current_pdf_path,
            pdf_name=self.current_pdf_name,
            start_time=self.session_start_time
        )

        # Start background thread to track elapsed time
        self.stop_event.clear()
        self.tracking_thread = Thread(target=self._tracking_loop, daemon=True)
        self.tracking_thread.start()

        if self.update_callback:
            self.update_callback()

    def stop_tracking(self):
        """Stop the current tracking session"""
        if not self.is_tracking:
            return

        self.is_tracking = False
        self.stop_event.set()

        if self.tracking_thread:
            self.tracking_thread.join(timeout=2)

        # End session in database
        if self.current_session_id:
            self.database.end_pdf_session(
                session_id=self.current_session_id,
                end_time=datetime.now()
            )

        self.current_session_id = None
        self.current_pdf_path = None
        self.current_pdf_name = None
        self.session_start_time = None

        if self.update_callback:
            self.update_callback()

    def _tracking_loop(self):
        """Background loop that updates tracking status"""
        while not self.stop_event.wait(timeout=1):
            if self.update_callback:
                self.update_callback()

    def get_current_duration(self) -> int:
        """Get current session duration in seconds

        Returns:
            Duration in seconds, or 0 if not tracking
        """
        if not self.is_tracking or not self.session_start_time:
            return 0

        elapsed = datetime.now() - self.session_start_time
        return int(elapsed.total_seconds())

    def get_current_status(self) -> dict:
        """Get current tracking status

        Returns:
            Dictionary with current tracking information
        """
        return {
            'is_tracking': self.is_tracking,
            'pdf_name': self.current_pdf_name,
            'pdf_path': self.current_pdf_path,
            'duration_seconds': self.get_current_duration()
        }


class PDFDirectoryMonitor(FileSystemEventHandler):
    """Monitors a directory for PDF file access"""

    def __init__(self, directory_path: str, pdf_tracker: PDFTracker):
        """Initialize directory monitor

        Args:
            directory_path: Path to directory to monitor
            pdf_tracker: PDFTracker instance to use when PDFs are accessed
        """
        super().__init__()
        self.directory_path = directory_path
        self.pdf_tracker = pdf_tracker
        self.observer = None
        self.last_modified_pdf = None
        self.last_modified_time = 0

    def on_modified(self, event):
        """Called when a file in the monitored directory is modified

        Args:
            event: File system event
        """
        if event.is_directory:
            return

        # Check if it's a PDF file
        if event.src_path.lower().endswith('.pdf'):
            # Avoid duplicate events (debounce)
            current_time = time.time()
            if (self.last_modified_pdf == event.src_path and
                current_time - self.last_modified_time < 2):
                return

            self.last_modified_pdf = event.src_path
            self.last_modified_time = current_time

            # Start tracking this PDF
            self.pdf_tracker.start_tracking(event.src_path)

    def on_opened(self, event):
        """Called when a file is opened

        Args:
            event: File system event
        """
        if event.is_directory:
            return

        if event.src_path.lower().endswith('.pdf'):
            self.pdf_tracker.start_tracking(event.src_path)

    def start_monitoring(self):
        """Start monitoring the directory"""
        if not os.path.exists(self.directory_path):
            raise ValueError(f"Directory does not exist: {self.directory_path}")

        self.observer = Observer()
        self.observer.schedule(self, self.directory_path, recursive=True)
        self.observer.start()

    def stop_monitoring(self):
        """Stop monitoring the directory"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
