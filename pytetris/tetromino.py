"""
Tetromino piece module for PyTetris.

This module implements all 7 Tetromino shapes with:
- Precomputed rotation states for performance
- Color coding for each piece type
- Position tracking and movement
- Random piece generation

Related PRD Requirements: REQ-1 (Pieces), REQ-2 (Movement)
"""

import random
from typing import List, Tuple


# Precomputed rotation states for all Tetromino pieces
# Each piece has 4 rotation states (0, 90, 180, 270 degrees)
# Format: List of (row_offset, col_offset) relative to piece position
PIECE_SHAPES = {
    'I': [
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # Horizontal
        [(0, 1), (1, 1), (2, 1), (3, 1)],  # Vertical
        [(1, 0), (1, 1), (1, 2), (1, 3)],  # Horizontal (shifted)
        [(0, 2), (1, 2), (2, 2), (3, 2)],  # Vertical (shifted)
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # Same
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # Same
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # Same
    ],
    'T': [
        [(0, 1), (1, 0), (1, 1), (1, 2)],  # T pointing up
        [(0, 1), (1, 1), (1, 2), (2, 1)],  # T pointing right
        [(1, 0), (1, 1), (1, 2), (2, 1)],  # T pointing down
        [(0, 1), (1, 0), (1, 1), (2, 1)],  # T pointing left
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],  # S horizontal
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # S vertical
        [(1, 1), (1, 2), (2, 0), (2, 1)],  # S horizontal (shifted)
        [(0, 1), (1, 1), (1, 2), (2, 2)],  # S vertical (shifted)
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],  # Z horizontal
        [(0, 2), (1, 1), (1, 2), (2, 1)],  # Z vertical
        [(1, 0), (1, 1), (2, 1), (2, 2)],  # Z horizontal (shifted)
        [(0, 1), (1, 0), (1, 1), (2, 0)],  # Z vertical (shifted)
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],  # J normal
        [(0, 1), (0, 2), (1, 1), (2, 1)],  # J rotated 90
        [(1, 0), (1, 1), (1, 2), (2, 2)],  # J rotated 180
        [(0, 1), (1, 1), (2, 0), (2, 1)],  # J rotated 270
    ],
    'L': [
        [(0, 2), (1, 0), (1, 1), (1, 2)],  # L normal
        [(0, 1), (1, 1), (2, 1), (2, 2)],  # L rotated 90
        [(1, 0), (1, 1), (1, 2), (2, 0)],  # L rotated 180
        [(0, 0), (0, 1), (1, 1), (2, 1)],  # L rotated 270
    ],
}

# Color mapping for each piece type
PIECE_COLORS = {
    'I': 'cyan',
    'O': 'yellow',
    'T': 'purple',
    'S': 'green',
    'Z': 'red',
    'J': 'blue',
    'L': 'orange',
}


class Tetromino:
    """
    Represents a Tetromino piece.

    Each Tetromino has a type (I, O, T, S, Z, J, L), color, position,
    and rotation state. Uses precomputed rotation states for performance.

    Attributes:
        type (str): Piece type ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
        color (str): Color associated with this piece type
        row (int): Current row position (top of piece)
        col (int): Current column position (left of piece)
        rotation_state (int): Current rotation (0-3)
        shape (List[Tuple[int, int]]): Current shape offsets
    """

    def __init__(self, piece_type: str, spawn_col: int = 3):
        """
        Initialize a Tetromino piece.

        Args:
            piece_type: Type of piece ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
            spawn_col: Initial column position (default: 3 for top-center)

        Raises:
            ValueError: If piece_type is not valid
        """
        if piece_type not in PIECE_SHAPES:
            raise ValueError(f"Invalid piece type: {piece_type}")

        self.type = piece_type
        self.color = PIECE_COLORS[piece_type]
        self.row = 0  # Spawn at top
        self.col = spawn_col  # Spawn at center-ish
        self.rotation_state = 0
        self.shape = PIECE_SHAPES[piece_type][0].copy()

    def move_left(self) -> None:
        """Move the piece one column to the left."""
        self.col -= 1

    def move_right(self) -> None:
        """Move the piece one column to the right."""
        self.col += 1

    def move_down(self) -> None:
        """Move the piece one row down."""
        self.row += 1

    def rotate_clockwise(self) -> None:
        """
        Rotate the piece 90 degrees clockwise.

        Uses precomputed rotation states for fast execution.
        """
        self.rotation_state = (self.rotation_state + 1) % 4
        self.shape = PIECE_SHAPES[self.type][self.rotation_state].copy()

    def rotate_counterclockwise(self) -> None:
        """
        Rotate the piece 90 degrees counterclockwise.

        Uses precomputed rotation states for fast execution.
        """
        self.rotation_state = (self.rotation_state - 1) % 4
        self.shape = PIECE_SHAPES[self.type][self.rotation_state].copy()

    def get_block_positions(self) -> List[Tuple[int, int]]:
        """
        Get absolute positions of all blocks in the piece.

        Returns:
            List of (row, col) tuples for each block's absolute position
        """
        positions = []
        for row_offset, col_offset in self.shape:
            abs_row = self.row + row_offset
            abs_col = self.col + col_offset
            positions.append((abs_row, abs_col))
        return positions


class TetrominoFactory:
    """
    Factory for creating random Tetromino pieces.

    Provides method to generate random pieces for game play.
    Uses standard 7-bag randomization (equal probability).
    """

    def __init__(self):
        """Initialize the factory."""
        self.piece_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

    def get_random_piece(self) -> Tetromino:
        """
        Generate a random Tetromino piece.

        Returns:
            A new Tetromino instance of random type
        """
        piece_type = random.choice(self.piece_types)
        return Tetromino(piece_type)
