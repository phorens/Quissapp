# Learning Tracker

A Python desktop application that helps you track your daily learning progress by monitoring PDF viewing time, creating flashcards, and exporting them directly to Anki.

## Features

### PDF Tracking
- Track time spent viewing PDF documents
- Manual PDF tracking with start/stop controls
- View daily statistics and session history
- See breakdown of time spent on each PDF

### Flashcard Management
- Create flashcards with front (question) and back (answer)
- Add optional source information (e.g., PDF filename)
- Export flashcards directly to Anki format (.apkg)
- Alternative CSV export for flexible importing
- Track which cards have been exported

### Daily Reminders
- Automatic reminders at 9:00 AM, 2:00 PM, and 8:00 PM
- System notifications to check your learning progress
- Mark daily check-ins to track consistency

### Statistics
- View daily learning time
- Track unique PDFs viewed
- Monitor flashcard creation and export status
- Historical data stored in SQLite database

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Starting the Application

Run the main script:
```bash
python main.py
```

The application will open with a tabbed interface.

### PDF Tracking Tab

1. Click "Start Tracking PDF" to select a PDF file
2. The timer will start automatically
3. Click "Stop Tracking" when you're done studying
4. View today's statistics in the lower panel

### Flashcards Tab

1. Enter the question in the "Front" field
2. Enter the answer in the "Back" field
3. Optionally add a source (e.g., the PDF name)
4. Click "Create Flashcard" to save

To export to Anki:
- Click "Export New Cards (.apkg)" to export only cards not yet exported
- Click "Export All Cards (.apkg)" to export all flashcards
- Click "Export as CSV" for CSV format

The .apkg files can be imported directly into Anki:
1. Open Anki
2. File → Import
3. Select the .apkg file
4. Cards will be added to a "Learning Tracker" deck

### Statistics Tab

View comprehensive statistics about your learning:
- Total time spent today
- PDFs viewed with time breakdown
- Flashcard creation statistics

Click "Refresh Statistics" to update the display.

### Settings Tab

- Test the reminder system
- Mark today as checked manually
- View app information

## File Structure

```
learning-tracker/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── database.py        # SQLite database operations
│   ├── pdf_tracker.py     # PDF viewing time tracking
│   ├── flashcard_manager.py  # Flashcard creation and Anki export
│   ├── reminder_system.py # Daily reminder functionality
│   └── gui.py             # Tkinter GUI interface
├── data/
│   └── learning_tracker.db  # SQLite database (created on first run)
└── exports/               # Exported Anki decks (created when exporting)
```

## Database Schema

The application uses SQLite to store all data locally:

- **pdf_sessions**: Tracks PDF viewing sessions with timestamps and duration
- **flashcards**: Stores flashcards with front, back, source, and export status
- **reminder_checks**: Records daily reminder check-ins

## Dependencies

- **genanki**: Creates Anki deck packages (.apkg files)
- **watchdog**: File system monitoring (for potential auto-tracking features)
- **plyer**: Cross-platform system notifications
- **Pillow**: Image processing support
- **tkinter**: GUI framework (included with Python)

## Tips for Best Results

1. **Consistent Tracking**: Start tracking when you begin reading and stop when you finish
2. **Create Flashcards While Learning**: Add flashcards immediately after learning new concepts
3. **Regular Exports**: Export to Anki regularly to keep your deck up-to-date
4. **Daily Check-ins**: Respond to reminders to build consistent learning habits
5. **Review Statistics**: Check your stats to identify learning patterns

## Troubleshooting

### Notifications Not Working
If system notifications don't appear, check your OS notification settings. The app will still function without notifications.

### Database Issues
If you encounter database errors, check that the `data/` directory exists and is writable. You can safely delete `data/learning_tracker.db` to start fresh (this will delete all history).

### Import Issues
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Future Enhancements

Potential features for future versions:
- Automatic PDF detection and tracking
- Weekly/monthly statistics and reports
- Goal setting and achievement tracking
- Integration with more learning platforms
- Dark mode theme
- Cloud sync for multiple devices

## License

This project is open source and available for personal use.

## Contributing

Contributions, issues, and feature requests are welcome!

## Support

For issues or questions, please check the documentation or open an issue in the repository.

---

**Happy Learning!** 📚✨
