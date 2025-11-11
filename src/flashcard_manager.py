"""Flashcard management and Anki export functionality"""

import os
import genanki
import random
from datetime import datetime
from typing import List, Optional


class FlashcardManager:
    """Manages flashcards and exports them to Anki format"""

    def __init__(self, database):
        """Initialize flashcard manager

        Args:
            database: Database instance for storing flashcard data
        """
        self.database = database

        # Create a unique model ID for Anki (should be consistent)
        self.model_id = 1607392319

        # Define the Anki note model (card template)
        self.model = genanki.Model(
            self.model_id,
            'Learning Tracker Basic Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Source'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '<div class="question">{{Question}}</div>',
                    'afmt': '''
                        <div class="question">{{Question}}</div>
                        <hr id="answer">
                        <div class="answer">{{Answer}}</div>
                        {{#Source}}
                        <div class="source"><small>Source: {{Source}}</small></div>
                        {{/Source}}
                    ''',
                },
            ],
            css='''
                .card {
                    font-family: arial;
                    font-size: 20px;
                    text-align: center;
                    color: black;
                    background-color: white;
                }
                .question {
                    font-size: 24px;
                    margin: 20px;
                }
                .answer {
                    font-size: 20px;
                    margin: 20px;
                }
                .source {
                    font-size: 14px;
                    color: #666;
                    margin-top: 20px;
                }
            '''
        )

    def create_flashcard(self, front: str, back: str, pdf_source: Optional[str] = None) -> int:
        """Create a new flashcard

        Args:
            front: Front of the card (question)
            back: Back of the card (answer)
            pdf_source: Optional PDF file the card is from

        Returns:
            Flashcard ID
        """
        return self.database.add_flashcard(front, back, pdf_source)

    def get_flashcards(self, exported: Optional[bool] = None) -> List[dict]:
        """Get flashcards from database

        Args:
            exported: Filter by export status (None = all, True = exported, False = not exported)

        Returns:
            List of flashcard dictionaries
        """
        return self.database.get_flashcards(exported)

    def export_to_anki(self, output_path: Optional[str] = None,
                       only_new: bool = True) -> str:
        """Export flashcards to Anki package file

        Args:
            output_path: Path for the output .apkg file (optional)
            only_new: If True, only export cards that haven't been exported yet

        Returns:
            Path to the created .apkg file
        """
        # Get flashcards to export
        flashcards = self.get_flashcards(exported=False if only_new else None)

        if not flashcards:
            raise ValueError("No flashcards to export")

        # Create output directory if needed
        if output_path is None:
            os.makedirs('exports', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'exports/learning_tracker_deck_{timestamp}.apkg'

        # Ensure .apkg extension
        if not output_path.endswith('.apkg'):
            output_path += '.apkg'

        # Create Anki deck with unique ID
        deck_id = random.randrange(1 << 30, 1 << 31)
        deck = genanki.Deck(deck_id, 'Learning Tracker')

        # Add flashcards to deck
        card_ids = []
        for card_data in flashcards:
            # Create Anki note
            note = genanki.Note(
                model=self.model,
                fields=[
                    card_data['front'],
                    card_data['back'],
                    card_data['pdf_source'] or ''
                ]
            )
            deck.add_note(note)
            card_ids.append(card_data['id'])

        # Create package and save
        package = genanki.Package(deck)
        package.write_to_file(output_path)

        # Mark cards as exported
        if only_new:
            self.database.mark_flashcards_exported(card_ids)

        return output_path

    def export_to_csv(self, output_path: Optional[str] = None,
                      only_new: bool = True) -> str:
        """Export flashcards to CSV format (alternative Anki import format)

        Args:
            output_path: Path for the output .csv file (optional)
            only_new: If True, only export cards that haven't been exported yet

        Returns:
            Path to the created .csv file
        """
        import csv

        # Get flashcards to export
        flashcards = self.get_flashcards(exported=False if only_new else None)

        if not flashcards:
            raise ValueError("No flashcards to export")

        # Create output directory if needed
        if output_path is None:
            os.makedirs('exports', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'exports/learning_tracker_flashcards_{timestamp}.csv'

        # Ensure .csv extension
        if not output_path.endswith('.csv'):
            output_path += '.csv'

        # Write to CSV
        card_ids = []
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            for card_data in flashcards:
                writer.writerow([
                    card_data['front'],
                    card_data['back'],
                    card_data['pdf_source'] or ''
                ])
                card_ids.append(card_data['id'])

        # Mark cards as exported
        if only_new:
            self.database.mark_flashcards_exported(card_ids)

        return output_path

    def get_statistics(self) -> dict:
        """Get flashcard statistics

        Returns:
            Dictionary with statistics
        """
        all_cards = self.database.get_flashcards()
        exported_cards = self.database.get_flashcards(exported=True)
        new_cards = self.database.get_flashcards(exported=False)

        return {
            'total': len(all_cards),
            'exported': len(exported_cards),
            'new': len(new_cards)
        }
