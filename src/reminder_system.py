"""Daily reminder system for learning tracking"""

import time
from datetime import datetime, time as dt_time
from threading import Thread, Event
from typing import Optional, Callable
try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False


class ReminderSystem:
    """Manages daily reminders to check learning progress"""

    def __init__(self, database, reminder_callback: Optional[Callable] = None):
        """Initialize reminder system

        Args:
            database: Database instance for tracking reminder checks
            reminder_callback: Optional callback function when reminder triggers
        """
        self.database = database
        self.reminder_callback = reminder_callback
        self.is_running = False
        self.reminder_thread = None
        self.stop_event = Event()

        # Default reminder times (can be customized)
        self.reminder_times = [
            dt_time(9, 0),   # 9:00 AM
            dt_time(14, 0),  # 2:00 PM
            dt_time(20, 0),  # 8:00 PM
        ]

        self.last_reminder_date = None
        self.reminders_sent_today = set()

    def start(self):
        """Start the reminder system"""
        if self.is_running:
            return

        self.is_running = True
        self.stop_event.clear()
        self.reminder_thread = Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()

    def stop(self):
        """Stop the reminder system"""
        if not self.is_running:
            return

        self.is_running = False
        self.stop_event.set()

        if self.reminder_thread:
            self.reminder_thread.join(timeout=2)

    def _reminder_loop(self):
        """Background loop that checks for reminder times"""
        while not self.stop_event.wait(timeout=60):  # Check every minute
            current_time = datetime.now().time()
            current_date = datetime.now().date()

            # Reset daily tracking if it's a new day
            if self.last_reminder_date != current_date:
                self.last_reminder_date = current_date
                self.reminders_sent_today.clear()

            # Check if we should send a reminder
            for reminder_time in self.reminder_times:
                # Create a time window (5 minutes)
                time_key = f"{reminder_time.hour}:{reminder_time.minute}"

                if time_key not in self.reminders_sent_today:
                    # Check if current time is within the reminder window
                    current_minutes = current_time.hour * 60 + current_time.minute
                    reminder_minutes = reminder_time.hour * 60 + reminder_time.minute

                    if abs(current_minutes - reminder_minutes) < 5:
                        # Check if already checked today
                        if not self.database.was_checked_today():
                            self._send_reminder()
                            self.reminders_sent_today.add(time_key)

    def _send_reminder(self):
        """Send a reminder notification"""
        # Try to send system notification
        if NOTIFICATIONS_AVAILABLE:
            try:
                notification.notify(
                    title='Learning Tracker Reminder',
                    message='Time to check your learning progress for today!',
                    app_name='Learning Tracker',
                    timeout=10
                )
            except Exception as e:
                print(f"Failed to send notification: {e}")

        # Call callback if provided
        if self.reminder_callback:
            self.reminder_callback()

    def mark_checked(self):
        """Mark today's reminder as checked"""
        self.database.mark_daily_check()

    def set_reminder_times(self, times: list):
        """Set custom reminder times

        Args:
            times: List of datetime.time objects
        """
        self.reminder_times = times

    def get_reminder_times(self) -> list:
        """Get current reminder times

        Returns:
            List of datetime.time objects
        """
        return self.reminder_times.copy()

    def is_checked_today(self) -> bool:
        """Check if today's reminder was already checked

        Returns:
            True if checked, False otherwise
        """
        return self.database.was_checked_today()

    def send_test_reminder(self):
        """Send a test reminder (for testing purposes)"""
        self._send_reminder()
