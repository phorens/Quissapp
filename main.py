#!/usr/bin/env python3
"""
Learning Tracker - Main Application Entry Point

Track your daily learning by monitoring PDF viewing time,
create flashcards, and export them to Anki.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import Database
from pdf_tracker import PDFTracker
from flashcard_manager import FlashcardManager
from reminder_system import ReminderSystem
from gui import LearningTrackerGUI


def main():
    """Main entry point for the application"""
    print("Starting Learning Tracker...")

    # Initialize components
    database = Database()
    pdf_tracker = PDFTracker(database)
    flashcard_manager = FlashcardManager(database)
    reminder_system = ReminderSystem(database)

    # Create and run GUI
    try:
        app = LearningTrackerGUI(
            database=database,
            pdf_tracker=pdf_tracker,
            flashcard_manager=flashcard_manager,
            reminder_system=reminder_system
        )
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Cleanup
        pdf_tracker.stop_tracking()
        reminder_system.stop()
        database.close()
        print("Learning Tracker closed.")


if __name__ == "__main__":
    main()
