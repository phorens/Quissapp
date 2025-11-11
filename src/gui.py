"""GUI interface for Learning Tracker using Tkinter"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
from typing import Optional


class LearningTrackerGUI:
    """Main GUI application for Learning Tracker"""

    def __init__(self, database, pdf_tracker, flashcard_manager, reminder_system):
        """Initialize the GUI

        Args:
            database: Database instance
            pdf_tracker: PDFTracker instance
            flashcard_manager: FlashcardManager instance
            reminder_system: ReminderSystem instance
        """
        self.database = database
        self.pdf_tracker = pdf_tracker
        self.flashcard_manager = flashcard_manager
        self.reminder_system = reminder_system

        # Set update callback for PDF tracker
        self.pdf_tracker.update_callback = self.update_tracking_display

        # Create main window
        self.root = tk.Tk()
        self.root.title("Learning Tracker")
        self.root.geometry("900x700")

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.create_tracking_tab()
        self.create_flashcards_tab()
        self.create_stats_tab()
        self.create_settings_tab()

        # Start reminder system
        self.reminder_system.start()

        # Check if reminder needs to be shown
        self.check_daily_reminder()

    def create_tracking_tab(self):
        """Create the PDF tracking tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='PDF Tracking')

        # Title
        title_label = ttk.Label(tab, text="PDF Learning Tracker",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Current tracking status frame
        status_frame = ttk.LabelFrame(tab, text="Current Session", padding=15)
        status_frame.pack(fill='x', padx=20, pady=10)

        self.tracking_status_label = ttk.Label(status_frame,
                                               text="No PDF being tracked",
                                               font=('Arial', 11))
        self.tracking_status_label.pack()

        self.tracking_time_label = ttk.Label(status_frame,
                                             text="Duration: 0:00:00",
                                             font=('Arial', 14, 'bold'))
        self.tracking_time_label.pack(pady=5)

        # Control buttons frame
        button_frame = ttk.Frame(tab)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Tracking PDF",
                                       command=self.start_tracking_pdf)
        self.start_button.pack(side='left', padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop Tracking",
                                      command=self.stop_tracking_pdf,
                                      state='disabled')
        self.stop_button.pack(side='left', padx=5)

        # Today's stats frame
        stats_frame = ttk.LabelFrame(tab, text="Today's Learning", padding=15)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.today_stats_label = ttk.Label(stats_frame, text="",
                                           font=('Arial', 10))
        self.today_stats_label.pack()

        # PDF list
        ttk.Label(stats_frame, text="PDFs viewed today:",
                 font=('Arial', 10, 'bold')).pack(pady=(10, 5))

        self.pdf_list_text = tk.Text(stats_frame, height=10, width=70,
                                     font=('Arial', 9))
        self.pdf_list_text.pack(pady=5)

        # Update display
        self.update_tracking_display()

    def create_flashcards_tab(self):
        """Create the flashcards management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Flashcards')

        # Title
        title_label = ttk.Label(tab, text="Flashcard Manager",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Create flashcard frame
        create_frame = ttk.LabelFrame(tab, text="Create New Flashcard", padding=15)
        create_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(create_frame, text="Front (Question):").grid(row=0, column=0,
                                                               sticky='w', pady=5)
        self.flashcard_front_text = tk.Text(create_frame, height=3, width=50)
        self.flashcard_front_text.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(create_frame, text="Back (Answer):").grid(row=2, column=0,
                                                            sticky='w', pady=5)
        self.flashcard_back_text = tk.Text(create_frame, height=3, width=50)
        self.flashcard_back_text.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(create_frame, text="Source (optional):").grid(row=4, column=0,
                                                                sticky='w', pady=5)
        self.flashcard_source_entry = ttk.Entry(create_frame, width=50)
        self.flashcard_source_entry.grid(row=5, column=0, pady=5)

        ttk.Button(create_frame, text="Create Flashcard",
                  command=self.create_flashcard).grid(row=5, column=1, padx=10)

        # Export frame
        export_frame = ttk.LabelFrame(tab, text="Export to Anki", padding=15)
        export_frame.pack(fill='x', padx=20, pady=10)

        self.flashcard_stats_label = ttk.Label(export_frame, text="")
        self.flashcard_stats_label.pack()

        button_frame = ttk.Frame(export_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Export New Cards (.apkg)",
                  command=self.export_to_anki).pack(side='left', padx=5)

        ttk.Button(button_frame, text="Export All Cards (.apkg)",
                  command=lambda: self.export_to_anki(only_new=False)).pack(side='left', padx=5)

        ttk.Button(button_frame, text="Export as CSV",
                  command=self.export_to_csv).pack(side='left', padx=5)

        # Flashcard list
        list_frame = ttk.LabelFrame(tab, text="Recent Flashcards", padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create treeview for flashcards
        columns = ('Front', 'Back', 'Source', 'Exported')
        self.flashcard_tree = ttk.Treeview(list_frame, columns=columns,
                                           show='headings', height=10)

        self.flashcard_tree.heading('Front', text='Front')
        self.flashcard_tree.heading('Back', text='Back')
        self.flashcard_tree.heading('Source', text='Source')
        self.flashcard_tree.heading('Exported', text='Exported')

        self.flashcard_tree.column('Front', width=200)
        self.flashcard_tree.column('Back', width=200)
        self.flashcard_tree.column('Source', width=150)
        self.flashcard_tree.column('Exported', width=80)

        self.flashcard_tree.pack(fill='both', expand=True)

        # Update display
        self.update_flashcard_display()

    def create_stats_tab(self):
        """Create the statistics tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Statistics')

        # Title
        title_label = ttk.Label(tab, text="Learning Statistics",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Stats display
        stats_frame = ttk.LabelFrame(tab, text="Overview", padding=15)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.stats_text = tk.Text(stats_frame, height=20, width=70,
                                 font=('Arial', 10))
        self.stats_text.pack(fill='both', expand=True)

        # Refresh button
        ttk.Button(tab, text="Refresh Statistics",
                  command=self.update_stats_display).pack(pady=10)

        # Update display
        self.update_stats_display()

    def create_settings_tab(self):
        """Create the settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Settings')

        # Title
        title_label = ttk.Label(tab, text="Settings",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Reminder settings
        reminder_frame = ttk.LabelFrame(tab, text="Daily Reminders", padding=15)
        reminder_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(reminder_frame,
                 text="Reminders are sent at 9:00 AM, 2:00 PM, and 8:00 PM").pack()

        ttk.Button(reminder_frame, text="Test Reminder",
                  command=self.test_reminder).pack(pady=10)

        ttk.Button(reminder_frame, text="Mark Today as Checked",
                  command=self.mark_reminder_checked).pack(pady=5)

        # About
        about_frame = ttk.LabelFrame(tab, text="About", padding=15)
        about_frame.pack(fill='x', padx=20, pady=10)

        about_text = """Learning Tracker v1.0

Track your daily learning by monitoring PDF viewing time.
Create flashcards and export them directly to Anki.
Get daily reminders to check your progress.

Built with Python and Tkinter."""

        ttk.Label(about_frame, text=about_text, justify='left').pack()

    def start_tracking_pdf(self):
        """Start tracking a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF to track",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if file_path:
            self.pdf_tracker.start_tracking(file_path)
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')

    def stop_tracking_pdf(self):
        """Stop tracking the current PDF"""
        self.pdf_tracker.stop_tracking()
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def update_tracking_display(self):
        """Update the tracking display with current information"""
        status = self.pdf_tracker.get_current_status()

        if status['is_tracking']:
            self.tracking_status_label.config(
                text=f"Currently tracking: {status['pdf_name']}"
            )

            # Format duration
            seconds = status['duration_seconds']
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60

            self.tracking_time_label.config(
                text=f"Duration: {hours}:{minutes:02d}:{secs:02d}"
            )
        else:
            self.tracking_status_label.config(text="No PDF being tracked")
            self.tracking_time_label.config(text="Duration: 0:00:00")

        # Update today's stats
        stats = self.database.get_daily_stats()
        stats_text = (f"Total time today: {stats['hours']} hours {stats['minutes']} minutes\n"
                     f"PDFs viewed: {stats['unique_pdfs']} | "
                     f"Sessions: {stats['total_sessions']}")
        self.today_stats_label.config(text=stats_text)

        # Update PDF list
        pdf_list = self.database.get_pdf_list_for_date()
        self.pdf_list_text.delete('1.0', tk.END)

        if pdf_list:
            for pdf_name, total_seconds in pdf_list:
                minutes = total_seconds // 60
                hours = minutes // 60
                mins = minutes % 60
                self.pdf_list_text.insert(tk.END,
                    f"{pdf_name}: {hours}h {mins}m\n")
        else:
            self.pdf_list_text.insert(tk.END, "No PDFs viewed today")

    def create_flashcard(self):
        """Create a new flashcard"""
        front = self.flashcard_front_text.get('1.0', tk.END).strip()
        back = self.flashcard_back_text.get('1.0', tk.END).strip()
        source = self.flashcard_source_entry.get().strip()

        if not front or not back:
            messagebox.showwarning("Incomplete Flashcard",
                                  "Please fill in both front and back of the card.")
            return

        self.flashcard_manager.create_flashcard(
            front=front,
            back=back,
            pdf_source=source if source else None
        )

        # Clear inputs
        self.flashcard_front_text.delete('1.0', tk.END)
        self.flashcard_back_text.delete('1.0', tk.END)
        self.flashcard_source_entry.delete(0, tk.END)

        # Update display
        self.update_flashcard_display()

        messagebox.showinfo("Success", "Flashcard created successfully!")

    def export_to_anki(self, only_new: bool = True):
        """Export flashcards to Anki format"""
        try:
            output_path = self.flashcard_manager.export_to_anki(only_new=only_new)
            messagebox.showinfo("Success",
                              f"Flashcards exported successfully!\n\n"
                              f"File: {output_path}\n\n"
                              f"Import this file in Anki to add the cards.")
            self.update_flashcard_display()
        except ValueError as e:
            messagebox.showwarning("No Cards", str(e))
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export: {e}")

    def export_to_csv(self):
        """Export flashcards to CSV format"""
        try:
            output_path = self.flashcard_manager.export_to_csv(only_new=True)
            messagebox.showinfo("Success",
                              f"Flashcards exported to CSV!\n\n"
                              f"File: {output_path}")
            self.update_flashcard_display()
        except ValueError as e:
            messagebox.showwarning("No Cards", str(e))
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export: {e}")

    def update_flashcard_display(self):
        """Update the flashcard display"""
        # Update statistics
        stats = self.flashcard_manager.get_statistics()
        self.flashcard_stats_label.config(
            text=f"Total: {stats['total']} cards | "
                 f"New: {stats['new']} | Exported: {stats['exported']}"
        )

        # Update treeview
        for item in self.flashcard_tree.get_children():
            self.flashcard_tree.delete(item)

        flashcards = self.flashcard_manager.get_flashcards()
        for card in flashcards[:20]:  # Show last 20
            # Truncate long text
            front = card['front'][:50] + '...' if len(card['front']) > 50 else card['front']
            back = card['back'][:50] + '...' if len(card['back']) > 50 else card['back']
            source = card['pdf_source'] or '-'
            exported = 'Yes' if card['exported'] else 'No'

            self.flashcard_tree.insert('', 0, values=(front, back, source, exported))

    def update_stats_display(self):
        """Update the statistics display"""
        self.stats_text.delete('1.0', tk.END)

        # Get today's stats
        stats = self.database.get_daily_stats()

        self.stats_text.insert(tk.END, "=== TODAY'S LEARNING ===\n\n")
        self.stats_text.insert(tk.END,
            f"Total time: {stats['hours']} hours {stats['minutes']} minutes\n")
        self.stats_text.insert(tk.END,
            f"Unique PDFs: {stats['unique_pdfs']}\n")
        self.stats_text.insert(tk.END,
            f"Total sessions: {stats['total_sessions']}\n\n")

        # PDF breakdown
        self.stats_text.insert(tk.END, "=== PDF BREAKDOWN ===\n\n")
        pdf_list = self.database.get_pdf_list_for_date()

        if pdf_list:
            for pdf_name, total_seconds in pdf_list:
                minutes = total_seconds // 60
                hours = minutes // 60
                mins = minutes % 60
                self.stats_text.insert(tk.END,
                    f"{pdf_name}\n  Time: {hours}h {mins}m\n\n")
        else:
            self.stats_text.insert(tk.END, "No PDFs viewed today\n\n")

        # Flashcard stats
        card_stats = self.flashcard_manager.get_statistics()
        self.stats_text.insert(tk.END, "=== FLASHCARDS ===\n\n")
        self.stats_text.insert(tk.END,
            f"Total flashcards: {card_stats['total']}\n")
        self.stats_text.insert(tk.END,
            f"New (not exported): {card_stats['new']}\n")
        self.stats_text.insert(tk.END,
            f"Exported to Anki: {card_stats['exported']}\n")

    def test_reminder(self):
        """Send a test reminder"""
        self.reminder_system.send_test_reminder()
        messagebox.showinfo("Test Reminder", "Test reminder sent!")

    def mark_reminder_checked(self):
        """Mark today's reminder as checked"""
        self.reminder_system.mark_checked()
        messagebox.showinfo("Marked", "Today marked as checked!")

    def check_daily_reminder(self):
        """Check if daily reminder should be shown"""
        if not self.reminder_system.is_checked_today():
            response = messagebox.askyesno(
                "Daily Reminder",
                "Have you checked your learning progress today?"
            )
            if response:
                self.reminder_system.mark_checked()

    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

    def cleanup(self):
        """Cleanup before closing"""
        self.pdf_tracker.stop_tracking()
        self.reminder_system.stop()
        self.database.close()
