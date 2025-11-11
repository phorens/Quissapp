"""Database module for storing learning data"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Tuple, Optional


class Database:
    """Handles all database operations for the learning tracker"""

    def __init__(self, db_path: str = "data/learning_tracker.db"):
        """Initialize database connection

        Args:
            db_path: Path to the SQLite database file
        """
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.conn = None
        self.initialize_database()

    def initialize_database(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Table for PDF tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdf_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_path TEXT NOT NULL,
                pdf_name TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                duration_seconds INTEGER,
                date TEXT NOT NULL
            )
        ''')

        # Table for flashcards
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                pdf_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                exported BOOLEAN DEFAULT 0
            )
        ''')

        # Table for daily reminders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminder_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_date TEXT NOT NULL UNIQUE,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def add_pdf_session(self, pdf_path: str, pdf_name: str, start_time: datetime) -> int:
        """Start a new PDF viewing session

        Args:
            pdf_path: Full path to the PDF file
            pdf_name: Name of the PDF file
            start_time: When the session started

        Returns:
            Session ID
        """
        cursor = self.conn.cursor()
        session_date = start_time.strftime('%Y-%m-%d')

        cursor.execute('''
            INSERT INTO pdf_sessions (pdf_path, pdf_name, start_time, date)
            VALUES (?, ?, ?, ?)
        ''', (pdf_path, pdf_name, start_time, session_date))

        self.conn.commit()
        return cursor.lastrowid

    def end_pdf_session(self, session_id: int, end_time: datetime):
        """End a PDF viewing session

        Args:
            session_id: ID of the session to end
            end_time: When the session ended
        """
        cursor = self.conn.cursor()

        # Get start time to calculate duration
        cursor.execute('SELECT start_time FROM pdf_sessions WHERE id = ?', (session_id,))
        result = cursor.fetchone()

        if result:
            start_time = datetime.fromisoformat(result[0])
            duration = int((end_time - start_time).total_seconds())

            cursor.execute('''
                UPDATE pdf_sessions
                SET end_time = ?, duration_seconds = ?
                WHERE id = ?
            ''', (end_time, duration, session_id))

            self.conn.commit()

    def get_daily_stats(self, target_date: Optional[str] = None) -> dict:
        """Get learning statistics for a specific date

        Args:
            target_date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            Dictionary with statistics
        """
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')

        cursor = self.conn.cursor()

        # Total time spent
        cursor.execute('''
            SELECT
                COALESCE(SUM(duration_seconds), 0) as total_seconds,
                COUNT(DISTINCT pdf_path) as unique_pdfs,
                COUNT(*) as total_sessions
            FROM pdf_sessions
            WHERE date = ? AND duration_seconds IS NOT NULL
        ''', (target_date,))

        result = cursor.fetchone()
        total_seconds = result[0]
        unique_pdfs = result[1]
        total_sessions = result[2]

        # Convert seconds to hours and minutes
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        return {
            'date': target_date,
            'total_seconds': total_seconds,
            'hours': hours,
            'minutes': minutes,
            'unique_pdfs': unique_pdfs,
            'total_sessions': total_sessions
        }

    def get_pdf_list_for_date(self, target_date: Optional[str] = None) -> List[Tuple]:
        """Get list of PDFs viewed on a specific date

        Args:
            target_date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            List of tuples (pdf_name, total_seconds)
        """
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')

        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT
                pdf_name,
                SUM(duration_seconds) as total_seconds
            FROM pdf_sessions
            WHERE date = ? AND duration_seconds IS NOT NULL
            GROUP BY pdf_name
            ORDER BY total_seconds DESC
        ''', (target_date,))

        return cursor.fetchall()

    def add_flashcard(self, front: str, back: str, pdf_source: Optional[str] = None) -> int:
        """Add a new flashcard

        Args:
            front: Front of the flashcard (question)
            back: Back of the flashcard (answer)
            pdf_source: Optional PDF file the flashcard is from

        Returns:
            Flashcard ID
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO flashcards (front, back, pdf_source)
            VALUES (?, ?, ?)
        ''', (front, back, pdf_source))

        self.conn.commit()
        return cursor.lastrowid

    def get_flashcards(self, exported: Optional[bool] = None) -> List[dict]:
        """Get flashcards

        Args:
            exported: Filter by export status (None = all, True = exported, False = not exported)

        Returns:
            List of flashcard dictionaries
        """
        cursor = self.conn.cursor()

        if exported is None:
            cursor.execute('''
                SELECT id, front, back, pdf_source, created_at, exported
                FROM flashcards
                ORDER BY created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, front, back, pdf_source, created_at, exported
                FROM flashcards
                WHERE exported = ?
                ORDER BY created_at DESC
            ''', (1 if exported else 0,))

        results = cursor.fetchall()

        flashcards = []
        for row in results:
            flashcards.append({
                'id': row[0],
                'front': row[1],
                'back': row[2],
                'pdf_source': row[3],
                'created_at': row[4],
                'exported': bool(row[5])
            })

        return flashcards

    def mark_flashcards_exported(self, flashcard_ids: List[int]):
        """Mark flashcards as exported

        Args:
            flashcard_ids: List of flashcard IDs to mark as exported
        """
        cursor = self.conn.cursor()
        placeholders = ','.join('?' * len(flashcard_ids))
        cursor.execute(f'''
            UPDATE flashcards
            SET exported = 1
            WHERE id IN ({placeholders})
        ''', flashcard_ids)

        self.conn.commit()

    def mark_daily_check(self, check_date: Optional[str] = None):
        """Record that the daily reminder was checked

        Args:
            check_date: Date in YYYY-MM-DD format (defaults to today)
        """
        if check_date is None:
            check_date = date.today().strftime('%Y-%m-%d')

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO reminder_checks (check_date, checked_at)
            VALUES (?, ?)
        ''', (check_date, datetime.now()))

        self.conn.commit()

    def was_checked_today(self) -> bool:
        """Check if daily reminder was already checked today

        Returns:
            True if checked, False otherwise
        """
        today = date.today().strftime('%Y-%m-%d')
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM reminder_checks WHERE check_date = ?
        ''', (today,))

        return cursor.fetchone()[0] > 0

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
