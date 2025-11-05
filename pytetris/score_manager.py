"""
Score management module for PyTetris.

This module implements scoring mechanics including:
- Line clear scoring with level-based multipliers
- Soft drop scoring
- Lines cleared tracking
- Level progression calculation
- High score persistence to JSON file

Related PRD Requirements: REQ-5 (Scoring), REQ-6 (Level Progression), REQ-10 (Score Persistence)
"""

import json
import os
from typing import Optional


class ScoreManager:
    """
    Manages game scoring, level progression, and high score persistence.

    Scoring rules (REQ-5):
    - Single line: 100 × level points
    - Double lines: 300 × level points
    - Triple lines: 500 × level points
    - Tetris (4 lines): 800 × level points
    - Soft drop: 1 point per cell descended

    Level progression (REQ-6):
    - Level = 1 + (lines_cleared // 10)

    Attributes:
        score (int): Current game score
        lines_cleared (int): Total lines cleared in current game
        level (int): Current level
        high_score (int): Best score across all games
        save_file (str): Path to JSON file for persisting high score
    """

    def __init__(self, save_file: str = 'pytetris_scores.json'):
        """
        Initialize the score manager.

        Args:
            save_file: Path to file for saving/loading high scores
        """
        self.score = 0
        self.lines_cleared = 0
        self.high_score = 0
        self.save_file = save_file

    def get_score(self) -> int:
        """
        Get the current score.

        Returns:
            Current score value
        """
        return self.score

    def get_lines_cleared(self) -> int:
        """
        Get the number of lines cleared.

        Returns:
            Total lines cleared in current game
        """
        return self.lines_cleared

    def get_level(self) -> int:
        """
        Get the current level.

        Level is calculated as: 1 + (lines_cleared // 10)
        This means level increases every 10 lines cleared.

        Returns:
            Current level (1-based)
        """
        return 1 + (self.lines_cleared // 10)

    def get_high_score(self) -> int:
        """
        Get the high score.

        Returns:
            Best score across all games
        """
        return self.high_score

    def set_level(self, level: int) -> None:
        """
        Set the level (for testing purposes).

        Note: In normal gameplay, level is calculated from lines_cleared.
        This method is primarily for testing scenarios.

        Args:
            level: Level to set
        """
        # Calculate lines_cleared that would result in this level
        # level = 1 + (lines_cleared // 10)
        # So: lines_cleared = (level - 1) * 10
        self.lines_cleared = (level - 1) * 10

    def add_line_clear_score(self, num_lines: int) -> None:
        """
        Add score for clearing lines.

        Scoring formula (REQ-5):
        - 1 line: 100 × level
        - 2 lines: 300 × level
        - 3 lines: 500 × level
        - 4 lines: 800 × level

        Args:
            num_lines: Number of lines cleared (1-4)
        """
        level = self.get_level()

        # Score lookup table
        points_map = {
            1: 100,   # Single
            2: 300,   # Double
            3: 500,   # Triple
            4: 800,   # Tetris
        }

        if num_lines in points_map:
            self.score += points_map[num_lines] * level
            self.lines_cleared += num_lines

    def add_soft_drop_score(self, cells: int) -> None:
        """
        Add score for soft drop.

        Awards 1 point per cell descended (REQ-5).

        Args:
            cells: Number of cells the piece descended
        """
        self.score += cells

    def update_high_score(self) -> None:
        """
        Update high score if current score exceeds it.

        High score only increases, never decreases (REQ-10).
        """
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self) -> None:
        """
        Reset score for a new game.

        Clears score and lines_cleared, but preserves high_score.
        """
        self.score = 0
        self.lines_cleared = 0

    def save(self) -> None:
        """
        Save high score to JSON file (REQ-10).

        Creates or overwrites the save file with current high score.
        Uses JSON format for human readability and easy extensibility.
        """
        try:
            data = {
                'high_score': self.high_score
            }
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
        except (IOError, OSError) as e:
            # Fail silently - don't crash game if save fails
            # Could log error in production
            pass

    def load(self) -> None:
        """
        Load high score from JSON file (REQ-10).

        If file doesn't exist or is invalid, starts with high_score = 0.
        Handles missing or corrupted files gracefully.
        """
        if not os.path.exists(self.save_file):
            # File doesn't exist yet - use default
            self.high_score = 0
            return

        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                self.high_score = data.get('high_score', 0)
        except (IOError, OSError, json.JSONDecodeError) as e:
            # Corrupted or unreadable file - use default
            self.high_score = 0
