"""GUI interface for Learning Tracker using Tkinter"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
from typing import Optional
import os


class LearningTrackerGUI:
    """Main GUI application for Learning Tracker"""

    def __init__(self, database, pdf_tracker, flashcard_manager, reminder_system, pdf_monitor=None):
        """Initialize the GUI

        Args:
            database: Database instance
            pdf_tracker: PDFTracker instance
            flashcard_manager: FlashcardManager instance
            reminder_system: ReminderSystem instance
            pdf_monitor: PDFDirectoryMonitor instance (optional)
        """
        self.database = database
        self.pdf_tracker = pdf_tracker
        self.flashcard_manager = flashcard_manager
        self.reminder_system = reminder_system
        self.pdf_monitor = pdf_monitor

        # Set update callback for PDF tracker
        self.pdf_tracker.update_callback = self.update_tracking_display

        # Create main window
        self.root = tk.Tk()
        self.root.title("📚 Learning Tracker")
        self.root.geometry("1000x750")
        self.root.minsize(900, 700)

        # Set color scheme
        self.colors = {
            'bg': '#f5f6fa',
            'fg': '#2c3e50',
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'card_bg': '#ffffff',
            'accent': '#9b59b6'
        }

        self.root.configure(bg=self.colors['bg'])

        # Configure custom styles
        self.setup_styles()

        # Create header
        self.create_header()

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Create tabs
        self.create_tracking_tab()
        self.create_flashcards_tab()
        self.create_stats_tab()
        self.create_settings_tab()

        # Start reminder system
        self.reminder_system.start()

        # Check if reminder needs to be shown
        self.root.after(1000, self.check_daily_reminder)

        # Check for updates on startup (after 2 seconds to not block UI)
        self.root.after(2000, self.check_for_updates_on_startup)

        # Load saved monitoring directory
        self.load_monitor_settings()

    def setup_styles(self):
        """Configure custom ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure notebook
        style.configure('Custom.TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['card_bg'],
                       foreground=self.colors['fg'],
                       padding=[20, 10],
                       font=('Segoe UI', 10))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])

        # Configure frames
        style.configure('Card.TFrame', background=self.colors['card_bg'], relief='flat')
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'],
                       font=('Segoe UI', 10))
        style.configure('CardLabel.TLabel', background=self.colors['card_bg'])

        # Configure label frames
        style.configure('TLabelframe', background=self.colors['bg'],
                       foreground=self.colors['fg'], borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['primary'])

        # Configure buttons
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10,
                       background=self.colors['primary'],
                       foreground='white')
        style.map('Primary.TButton',
                 background=[('active', '#2980b9')])

        style.configure('Success.TButton',
                       font=('Segoe UI', 10),
                       padding=10,
                       background=self.colors['success'],
                       foreground='white')

        style.configure('Danger.TButton',
                       font=('Segoe UI', 10),
                       padding=10,
                       background=self.colors['danger'],
                       foreground='white')

    def create_header(self):
        """Create application header"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill='x', padx=15, pady=(15, 10))
        header.pack_propagate(False)

        title_label = tk.Label(header, text="📚 Learning Tracker",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['primary'], fg='white')
        title_label.pack(side='left', padx=20, pady=20)

        subtitle_label = tk.Label(header, text="Track your learning progress",
                                 font=('Segoe UI', 11),
                                 bg=self.colors['primary'], fg='#ecf0f1')
        subtitle_label.pack(side='left', padx=(0, 20), pady=20)

    def create_tracking_tab(self):
        """Create the PDF tracking tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='📄 PDF Tracking')

        # Main container with padding
        container = ttk.Frame(tab)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Auto-monitoring section
        monitor_frame = tk.Frame(container, bg=self.colors['card_bg'],
                                relief='solid', borderwidth=1)
        monitor_frame.pack(fill='x', pady=(0, 15))

        monitor_inner = tk.Frame(monitor_frame, bg=self.colors['card_bg'])
        monitor_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(monitor_inner, text="🔍 Auto-Detection",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w')

        tk.Label(monitor_inner, text="Automatically track PDFs when you open them from a folder",
                font=('Segoe UI', 9),
                bg=self.colors['card_bg'], fg='#7f8c8d').pack(anchor='w', pady=(2, 10))

        button_row = tk.Frame(monitor_inner, bg=self.colors['card_bg'])
        button_row.pack(fill='x')

        self.monitor_dir_button = ttk.Button(button_row, text="Select Folder to Monitor",
                                            command=self.select_monitor_directory,
                                            style='Primary.TButton')
        self.monitor_dir_button.pack(side='left', padx=(0, 10))

        self.monitor_status_label = tk.Label(button_row, text="Not monitoring",
                                            font=('Segoe UI', 9),
                                            bg=self.colors['card_bg'], fg='#95a5a6')
        self.monitor_status_label.pack(side='left')

        # Manual tracking section
        manual_frame = tk.Frame(container, bg=self.colors['card_bg'],
                               relief='solid', borderwidth=1)
        manual_frame.pack(fill='x', pady=(0, 15))

        manual_inner = tk.Frame(manual_frame, bg=self.colors['card_bg'])
        manual_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(manual_inner, text="✋ Manual Tracking",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w')

        tk.Label(manual_inner, text="Manually select a PDF file to start tracking",
                font=('Segoe UI', 9),
                bg=self.colors['card_bg'], fg='#7f8c8d').pack(anchor='w', pady=(2, 10))

        # Current session display
        session_display = tk.Frame(manual_inner, bg='#ecf0f1', relief='flat')
        session_display.pack(fill='x', pady=(0, 10))

        session_inner = tk.Frame(session_display, bg='#ecf0f1')
        session_inner.pack(padx=15, pady=12)

        self.tracking_status_label = tk.Label(session_inner,
                                             text="No PDF being tracked",
                                             font=('Segoe UI', 11),
                                             bg='#ecf0f1', fg=self.colors['fg'])
        self.tracking_status_label.pack()

        self.tracking_time_label = tk.Label(session_inner,
                                           text="⏱️ 0:00:00",
                                           font=('Segoe UI', 18, 'bold'),
                                           bg='#ecf0f1', fg=self.colors['primary'])
        self.tracking_time_label.pack(pady=(5, 0))

        # Control buttons
        button_frame = tk.Frame(manual_inner, bg=self.colors['card_bg'])
        button_frame.pack()

        self.start_button = ttk.Button(button_frame, text="▶️ Start Tracking",
                                      command=self.start_tracking_pdf,
                                      style='Success.TButton')
        self.start_button.pack(side='left', padx=5)

        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop Tracking",
                                     command=self.stop_tracking_pdf,
                                     style='Danger.TButton',
                                     state='disabled')
        self.stop_button.pack(side='left', padx=5)

        # Today's stats section
        stats_frame = tk.Frame(container, bg=self.colors['card_bg'],
                              relief='solid', borderwidth=1)
        stats_frame.pack(fill='both', expand=True)

        stats_inner = tk.Frame(stats_frame, bg=self.colors['card_bg'])
        stats_inner.pack(fill='both', expand=True, padx=20, pady=15)

        tk.Label(stats_inner, text="📊 Today's Learning",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w')

        self.today_stats_label = tk.Label(stats_inner, text="",
                                         font=('Segoe UI', 10),
                                         bg=self.colors['card_bg'], fg=self.colors['fg'])
        self.today_stats_label.pack(anchor='w', pady=(5, 10))

        tk.Label(stats_inner, text="PDFs viewed today:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(5, 5))

        # PDF list with scrollbar
        list_container = tk.Frame(stats_inner, bg=self.colors['card_bg'])
        list_container.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')

        self.pdf_list_text = tk.Text(list_container, height=8,
                                     font=('Consolas', 9),
                                     bg='#f8f9fa', fg=self.colors['fg'],
                                     relief='flat', borderwidth=5)
        self.pdf_list_text.pack(side='left', fill='both', expand=True)
        self.pdf_list_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pdf_list_text.yview)

        # Update display
        self.update_tracking_display()

    def create_flashcards_tab(self):
        """Create the flashcards management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='🎴 Flashcards')

        container = ttk.Frame(tab)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Create flashcard section
        create_frame = tk.Frame(container, bg=self.colors['card_bg'],
                               relief='solid', borderwidth=1)
        create_frame.pack(fill='x', pady=(0, 15))

        create_inner = tk.Frame(create_frame, bg=self.colors['card_bg'])
        create_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(create_inner, text="✨ Create New Flashcard",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 10))

        # Front
        tk.Label(create_inner, text="Front (Question):",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(5, 2))

        self.flashcard_front_text = tk.Text(create_inner, height=3,
                                           font=('Segoe UI', 10),
                                           relief='solid', borderwidth=1)
        self.flashcard_front_text.pack(fill='x', pady=(0, 10))

        # Back
        tk.Label(create_inner, text="Back (Answer):",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(5, 2))

        self.flashcard_back_text = tk.Text(create_inner, height=3,
                                          font=('Segoe UI', 10),
                                          relief='solid', borderwidth=1)
        self.flashcard_back_text.pack(fill='x', pady=(0, 10))

        # Source
        source_frame = tk.Frame(create_inner, bg=self.colors['card_bg'])
        source_frame.pack(fill='x', pady=(5, 10))

        tk.Label(source_frame, text="Source (optional):",
                font=('Segoe UI', 10),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(side='left', padx=(0, 10))

        self.flashcard_source_entry = tk.Entry(source_frame,
                                              font=('Segoe UI', 10),
                                              relief='solid', borderwidth=1)
        self.flashcard_source_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        ttk.Button(source_frame, text="➕ Create",
                  command=self.create_flashcard,
                  style='Success.TButton').pack(side='right')

        # Export section
        export_frame = tk.Frame(container, bg=self.colors['card_bg'],
                               relief='solid', borderwidth=1)
        export_frame.pack(fill='x', pady=(0, 15))

        export_inner = tk.Frame(export_frame, bg=self.colors['card_bg'])
        export_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(export_inner, text="📤 Export to Anki",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w')

        self.flashcard_stats_label = tk.Label(export_inner, text="",
                                             font=('Segoe UI', 10),
                                             bg=self.colors['card_bg'], fg=self.colors['fg'])
        self.flashcard_stats_label.pack(anchor='w', pady=(5, 10))

        button_frame = tk.Frame(export_inner, bg=self.colors['card_bg'])
        button_frame.pack()

        ttk.Button(button_frame, text="📦 Export New (.apkg)",
                  command=self.export_to_anki,
                  style='Primary.TButton').pack(side='left', padx=5)

        ttk.Button(button_frame, text="📦 Export All (.apkg)",
                  command=lambda: self.export_to_anki(only_new=False),
                  style='Primary.TButton').pack(side='left', padx=5)

        ttk.Button(button_frame, text="📄 Export CSV",
                  command=self.export_to_csv).pack(side='left', padx=5)

        # Flashcard list
        list_frame = tk.Frame(container, bg=self.colors['card_bg'],
                             relief='solid', borderwidth=1)
        list_frame.pack(fill='both', expand=True)

        list_inner = tk.Frame(list_frame, bg=self.colors['card_bg'])
        list_inner.pack(fill='both', expand=True, padx=20, pady=15)

        tk.Label(list_inner, text="📋 Recent Flashcards",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 10))

        # Create treeview for flashcards
        tree_frame = tk.Frame(list_inner, bg=self.colors['card_bg'])
        tree_frame.pack(fill='both', expand=True)

        columns = ('Front', 'Back', 'Source', 'Exported')
        self.flashcard_tree = ttk.Treeview(tree_frame, columns=columns,
                                          show='headings', height=10)

        self.flashcard_tree.heading('Front', text='Front')
        self.flashcard_tree.heading('Back', text='Back')
        self.flashcard_tree.heading('Source', text='Source')
        self.flashcard_tree.heading('Exported', text='Status')

        self.flashcard_tree.column('Front', width=220)
        self.flashcard_tree.column('Back', width=220)
        self.flashcard_tree.column('Source', width=150)
        self.flashcard_tree.column('Exported', width=80)

        tree_scroll = tk.Scrollbar(tree_frame, command=self.flashcard_tree.yview)
        self.flashcard_tree.configure(yscrollcommand=tree_scroll.set)

        self.flashcard_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')

        # Update display
        self.update_flashcard_display()

    def create_stats_tab(self):
        """Create the statistics tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='📈 Statistics')

        container = ttk.Frame(tab)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(container, bg=self.colors['card_bg'],
                               relief='solid', borderwidth=1)
        header_frame.pack(fill='x', pady=(0, 15))

        header_inner = tk.Frame(header_frame, bg=self.colors['card_bg'])
        header_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(header_inner, text="📊 Learning Overview",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(side='left')

        ttk.Button(header_inner, text="🔄 Refresh",
                  command=self.update_stats_display).pack(side='right')

        # Stats display
        stats_frame = tk.Frame(container, bg=self.colors['card_bg'],
                              relief='solid', borderwidth=1)
        stats_frame.pack(fill='both', expand=True)

        stats_inner = tk.Frame(stats_frame, bg=self.colors['card_bg'])
        stats_inner.pack(fill='both', expand=True, padx=20, pady=15)

        # Text widget with scrollbar
        text_container = tk.Frame(stats_inner, bg=self.colors['card_bg'])
        text_container.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side='right', fill='y')

        self.stats_text = tk.Text(text_container,
                                 font=('Consolas', 10),
                                 bg='#f8f9fa', fg=self.colors['fg'],
                                 relief='flat', borderwidth=5)
        self.stats_text.pack(side='left', fill='both', expand=True)
        self.stats_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.stats_text.yview)

        # Update display
        self.update_stats_display()

    def create_settings_tab(self):
        """Create the settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='⚙️ Settings')

        container = ttk.Frame(tab)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Reminder settings
        reminder_frame = tk.Frame(container, bg=self.colors['card_bg'],
                                 relief='solid', borderwidth=1)
        reminder_frame.pack(fill='x', pady=(0, 15))

        reminder_inner = tk.Frame(reminder_frame, bg=self.colors['card_bg'])
        reminder_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(reminder_inner, text="🔔 Daily Reminders",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 10))

        tk.Label(reminder_inner,
                text="Get reminded to check your progress at 9:00 AM, 2:00 PM, and 8:00 PM",
                font=('Segoe UI', 10),
                bg=self.colors['card_bg'], fg='#7f8c8d').pack(anchor='w', pady=(0, 10))

        btn_frame = tk.Frame(reminder_inner, bg=self.colors['card_bg'])
        btn_frame.pack(anchor='w')

        ttk.Button(btn_frame, text="🔔 Test Reminder",
                  command=self.test_reminder).pack(side='left', padx=(0, 10))

        ttk.Button(btn_frame, text="✅ Mark as Checked",
                  command=self.mark_reminder_checked).pack(side='left')

        # Updates section
        update_frame = tk.Frame(container, bg=self.colors['card_bg'],
                               relief='solid', borderwidth=1)
        update_frame.pack(fill='x', pady=(0, 15))

        update_inner = tk.Frame(update_frame, bg=self.colors['card_bg'])
        update_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(update_inner, text="🔄 Automatic Updates",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 10))

        tk.Label(update_inner,
                text="Keep your app up to date with the latest features and bug fixes",
                font=('Segoe UI', 10),
                bg=self.colors['card_bg'], fg='#7f8c8d').pack(anchor='w', pady=(0, 10))

        # Current version
        version_frame = tk.Frame(update_inner, bg='#ecf0f1', relief='flat')
        version_frame.pack(fill='x', pady=(0, 10))

        version_inner = tk.Frame(version_frame, bg='#ecf0f1')
        version_inner.pack(padx=15, pady=10)

        tk.Label(version_inner, text="Current Version:",
                font=('Segoe UI', 10),
                bg='#ecf0f1', fg=self.colors['fg']).pack(side='left')

        self.version_label = tk.Label(version_inner, text="v2.0.0",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg='#ecf0f1', fg=self.colors['primary'])
        self.version_label.pack(side='left', padx=(10, 0))

        # Update status
        self.update_status_label = tk.Label(update_inner, text="",
                                           font=('Segoe UI', 9),
                                           bg=self.colors['card_bg'], fg='#7f8c8d')
        self.update_status_label.pack(anchor='w', pady=(0, 10))

        # Update buttons
        update_btn_frame = tk.Frame(update_inner, bg=self.colors['card_bg'])
        update_btn_frame.pack(anchor='w')

        ttk.Button(update_btn_frame, text="🔍 Check for Updates",
                  command=self.check_for_updates).pack(side='left', padx=(0, 10))

        # Auto-check toggle
        self.auto_update_var = tk.BooleanVar(value=True)
        self.auto_update_check = tk.Checkbutton(update_btn_frame,
                                                text="Check automatically on startup",
                                                variable=self.auto_update_var,
                                                command=self.toggle_auto_update,
                                                font=('Segoe UI', 9),
                                                bg=self.colors['card_bg'],
                                                fg=self.colors['fg'],
                                                selectcolor='#ecf0f1')
        self.auto_update_check.pack(side='left')

        # Load auto-update setting
        self.load_auto_update_setting()

        # About
        about_frame = tk.Frame(container, bg=self.colors['card_bg'],
                              relief='solid', borderwidth=1)
        about_frame.pack(fill='x')

        about_inner = tk.Frame(about_frame, bg=self.colors['card_bg'])
        about_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(about_inner, text="ℹ️ About",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 10))

        about_text = """Learning Tracker v2.0

Track your daily learning by monitoring PDF viewing time.
Create flashcards and export them directly to Anki.
Get daily reminders to check your progress.

Built with Python and Tkinter."""

        tk.Label(about_inner, text=about_text, justify='left',
                font=('Segoe UI', 10),
                bg=self.colors['card_bg'], fg=self.colors['fg']).pack(anchor='w')

    def select_monitor_directory(self):
        """Select directory to monitor for PDFs"""
        directory = filedialog.askdirectory(
            title="Select folder containing your PDFs"
        )

        if directory:
            # Save directory preference
            self.save_monitor_directory(directory)

            # Start monitoring
            if self.pdf_monitor:
                try:
                    self.pdf_monitor.stop_monitoring()
                except:
                    pass

            # Import here to avoid circular import
            from pdf_tracker import PDFDirectoryMonitor

            self.pdf_monitor = PDFDirectoryMonitor(directory, self.pdf_tracker)
            try:
                self.pdf_monitor.start_monitoring()
                self.monitor_status_label.config(
                    text=f"✅ Monitoring: {os.path.basename(directory)}",
                    fg=self.colors['success']
                )
                messagebox.showinfo("Auto-Detection Started",
                                  f"Now monitoring:\n{directory}\n\n"
                                  "PDFs opened from this folder will be tracked automatically!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start monitoring: {e}")

    def save_monitor_directory(self, directory):
        """Save monitoring directory to file"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/monitor_dir.txt', 'w') as f:
                f.write(directory)
        except:
            pass

    def load_monitor_settings(self):
        """Load and restore monitoring settings"""
        try:
            if os.path.exists('data/monitor_dir.txt'):
                with open('data/monitor_dir.txt', 'r') as f:
                    directory = f.read().strip()
                    if os.path.exists(directory):
                        # Import here to avoid issues
                        from pdf_tracker import PDFDirectoryMonitor

                        self.pdf_monitor = PDFDirectoryMonitor(directory, self.pdf_tracker)
                        self.pdf_monitor.start_monitoring()
                        self.monitor_status_label.config(
                            text=f"✅ Monitoring: {os.path.basename(directory)}",
                            fg=self.colors['success']
                        )
        except:
            pass

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
                text=f"📖 Currently tracking: {status['pdf_name']}"
            )

            # Format duration
            seconds = status['duration_seconds']
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60

            self.tracking_time_label.config(
                text=f"⏱️ {hours}:{minutes:02d}:{secs:02d}"
            )
        else:
            self.tracking_status_label.config(text="No PDF being tracked")
            self.tracking_time_label.config(text="⏱️ 0:00:00")

        # Update today's stats
        stats = self.database.get_daily_stats()
        stats_text = (f"⏰ Total time: {stats['hours']}h {stats['minutes']}m  |  "
                     f"📚 PDFs: {stats['unique_pdfs']}  |  "
                     f"📊 Sessions: {stats['total_sessions']}")
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
                    f"📄 {pdf_name:<40} {hours}h {mins}m\n")
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

        messagebox.showinfo("Success", "✅ Flashcard created successfully!")

    def export_to_anki(self, only_new: bool = True):
        """Export flashcards to Anki format"""
        try:
            output_path = self.flashcard_manager.export_to_anki(only_new=only_new)
            messagebox.showinfo("Export Successful",
                              f"✅ Flashcards exported!\n\n"
                              f"File: {output_path}\n\n"
                              f"📥 Import this file in Anki to add the cards.")
            self.update_flashcard_display()
        except ValueError as e:
            messagebox.showwarning("No Cards", str(e))
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export: {e}")

    def export_to_csv(self):
        """Export flashcards to CSV format"""
        try:
            output_path = self.flashcard_manager.export_to_csv(only_new=True)
            messagebox.showinfo("Export Successful",
                              f"✅ Flashcards exported to CSV!\n\n"
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
            text=f"📊 Total: {stats['total']} cards  |  "
                 f"🆕 New: {stats['new']}  |  "
                 f"✅ Exported: {stats['exported']}"
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
            exported = '✅ Exported' if card['exported'] else '🆕 New'

            self.flashcard_tree.insert('', 0, values=(front, back, source, exported))

    def update_stats_display(self):
        """Update the statistics display"""
        self.stats_text.delete('1.0', tk.END)

        # Get today's stats
        stats = self.database.get_daily_stats()

        self.stats_text.insert(tk.END, "╔═══════════════════════════════════════╗\n")
        self.stats_text.insert(tk.END, "║     📚 TODAY'S LEARNING SUMMARY       ║\n")
        self.stats_text.insert(tk.END, "╚═══════════════════════════════════════╝\n\n")

        self.stats_text.insert(tk.END, f"⏰ Total Time:       {stats['hours']}h {stats['minutes']}m\n")
        self.stats_text.insert(tk.END, f"📚 Unique PDFs:      {stats['unique_pdfs']}\n")
        self.stats_text.insert(tk.END, f"📊 Total Sessions:   {stats['total_sessions']}\n\n")

        # PDF breakdown
        self.stats_text.insert(tk.END, "╔═══════════════════════════════════════╗\n")
        self.stats_text.insert(tk.END, "║        📄 PDF TIME BREAKDOWN          ║\n")
        self.stats_text.insert(tk.END, "╚═══════════════════════════════════════╝\n\n")

        pdf_list = self.database.get_pdf_list_for_date()

        if pdf_list:
            for pdf_name, total_seconds in pdf_list:
                minutes = total_seconds // 60
                hours = minutes // 60
                mins = minutes % 60

                # Truncate long names
                display_name = pdf_name[:35] + '...' if len(pdf_name) > 35 else pdf_name
                self.stats_text.insert(tk.END, f"  📖 {display_name}\n")
                self.stats_text.insert(tk.END, f"     ⏱️  {hours}h {mins}m\n\n")
        else:
            self.stats_text.insert(tk.END, "  No PDFs viewed today\n\n")

        # Flashcard stats
        card_stats = self.flashcard_manager.get_statistics()
        self.stats_text.insert(tk.END, "╔═══════════════════════════════════════╗\n")
        self.stats_text.insert(tk.END, "║          🎴 FLASHCARD STATS           ║\n")
        self.stats_text.insert(tk.END, "╚═══════════════════════════════════════╝\n\n")

        self.stats_text.insert(tk.END, f"📊 Total Cards:      {card_stats['total']}\n")
        self.stats_text.insert(tk.END, f"🆕 New Cards:        {card_stats['new']}\n")
        self.stats_text.insert(tk.END, f"✅ Exported to Anki: {card_stats['exported']}\n")

    def test_reminder(self):
        """Send a test reminder"""
        self.reminder_system.send_test_reminder()
        messagebox.showinfo("Test Reminder", "🔔 Test reminder sent!")

    def mark_reminder_checked(self):
        """Mark today's reminder as checked"""
        self.reminder_system.mark_checked()
        messagebox.showinfo("Marked", "✅ Today marked as checked!")

    def check_daily_reminder(self):
        """Check if daily reminder should be shown"""
        if not self.reminder_system.is_checked_today():
            response = messagebox.askyesno(
                "📚 Daily Learning Check",
                "Have you checked your learning progress today?\n\n"
                "Review your stats to see how much you've learned!"
            )
            if response:
                self.reminder_system.mark_checked()

    def load_auto_update_setting(self):
        """Load auto-update setting from updater"""
        try:
            from updater import UpdateChecker
            updater = UpdateChecker()
            settings = updater.get_update_settings()
            self.auto_update_var.set(settings.get("auto_check", True))
        except:
            pass

    def toggle_auto_update(self):
        """Toggle auto-update setting"""
        try:
            from updater import UpdateChecker
            updater = UpdateChecker()
            settings = updater.get_update_settings()
            settings["auto_check"] = self.auto_update_var.get()
            updater.save_update_settings(settings)
        except:
            pass

    def check_for_updates(self):
        """Check for app updates"""
        self.update_status_label.config(text="🔍 Checking for updates...", fg='#7f8c8d')
        self.root.update()

        try:
            from updater import UpdateChecker
            updater = UpdateChecker()

            update_info = updater.check_for_updates()

            if update_info:
                # Update available
                self.update_status_label.config(
                    text=f"✨ Update available: v{update_info['version']}",
                    fg=self.colors['success']
                )

                # Ask user if they want to install
                response = messagebox.askyesno(
                    "Update Available",
                    f"A new version is available!\n\n"
                    f"Current: v{updater.get_current_version()}\n"
                    f"Latest: v{update_info['version']}\n\n"
                    f"Release Notes:\n{update_info['release_notes'][:200]}...\n\n"
                    f"Would you like to install this update now?\n\n"
                    f"(The app will restart after installation)"
                )

                if response:
                    self.install_update(update_info)
            else:
                # No update available
                self.update_status_label.config(
                    text="✅ You're running the latest version!",
                    fg=self.colors['success']
                )
                messagebox.showinfo("No Updates",
                                   f"You're already running the latest version (v{updater.get_current_version()})")

        except Exception as e:
            self.update_status_label.config(
                text=f"❌ Update check failed: {str(e)}",
                fg=self.colors['danger']
            )
            messagebox.showerror("Update Check Failed",
                               f"Failed to check for updates:\n{str(e)}\n\n"
                               f"Please check your internet connection.")

    def install_update(self, update_info):
        """Install an update"""
        # Create progress dialog
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("Installing Update")
        progress_dialog.geometry("400x150")
        progress_dialog.resizable(False, False)
        progress_dialog.transient(self.root)
        progress_dialog.grab_set()

        # Center the dialog
        progress_dialog.update_idletasks()
        x = (progress_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_dialog.winfo_screenheight() // 2) - (150 // 2)
        progress_dialog.geometry(f"400x150+{x}+{y}")

        tk.Label(progress_dialog, text="Installing update...",
                font=('Segoe UI', 12, 'bold')).pack(pady=20)

        progress_label = tk.Label(progress_dialog, text="Preparing...",
                                 font=('Segoe UI', 10))
        progress_label.pack()

        from tkinter import ttk as tkttk
        progress_bar = tkttk.Progressbar(progress_dialog, length=350,
                                        mode='determinate')
        progress_bar.pack(pady=20)

        def update_progress(percentage):
            """Update progress bar"""
            progress_bar['value'] = percentage
            if percentage < 40:
                progress_label.config(text="Downloading update...")
            elif percentage < 80:
                progress_label.config(text="Extracting files...")
            elif percentage < 95:
                progress_label.config(text="Installing files...")
            else:
                progress_label.config(text="Finalizing...")
            progress_dialog.update()

        # Install update in background
        def do_install():
            try:
                from updater import UpdateChecker
                updater = UpdateChecker()

                success, message = updater.download_and_install_update(
                    update_info['download_url'],
                    progress_callback=update_progress
                )

                progress_dialog.destroy()

                if success:
                    result = messagebox.showinfo("Update Complete",
                                                f"{message}\n\n"
                                                f"The application will now close.\n"
                                                f"Please restart it to use the new version.")
                    # Close the app
                    self.root.quit()
                else:
                    messagebox.showerror("Update Failed", message)
                    self.update_status_label.config(
                        text="❌ Update installation failed",
                        fg=self.colors['danger']
                    )

            except Exception as e:
                progress_dialog.destroy()
                messagebox.showerror("Update Failed",
                                   f"Failed to install update:\n{str(e)}")
                self.update_status_label.config(
                    text="❌ Update installation failed",
                    fg=self.colors['danger']
                )

        # Run installation in thread to keep UI responsive
        import threading
        install_thread = threading.Thread(target=do_install, daemon=True)
        install_thread.start()

    def check_for_updates_on_startup(self):
        """Check for updates on startup if enabled"""
        try:
            from updater import UpdateChecker
            updater = UpdateChecker()

            if updater.should_check_for_updates():
                update_info = updater.check_for_updates()

                if update_info:
                    response = messagebox.askyesno(
                        "🎉 Update Available",
                        f"A new version of Learning Tracker is available!\n\n"
                        f"Current: v{updater.get_current_version()}\n"
                        f"Latest: v{update_info['version']}\n\n"
                        f"Would you like to view the updates section?"
                    )

                    if response:
                        # Switch to settings tab
                        self.notebook.select(3)  # Settings is the 4th tab
                        self.update_status_label.config(
                            text=f"✨ Update available: v{update_info['version']}",
                            fg=self.colors['success']
                        )
        except:
            # Silently fail - don't bother user on startup
            pass

    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

    def cleanup(self):
        """Cleanup before closing"""
        self.pdf_tracker.stop_tracking()
        if self.pdf_monitor:
            self.pdf_monitor.stop_monitoring()
        self.reminder_system.stop()
        self.database.close()
