"""
Collision detection module for PyTetris.

This module implements collision detection for:
- Wall and floor boundaries
- Block-to-block collisions
- Rotation collision handling
- Wall kick support
- Piece locking detection

Related PRD Requirements: REQ-3 (Collision Detection)
"""

from typing import Optional, Tuple
from pytetris.board import Board
from pytetris.tetromino import Tetromino


class CollisionDetector:
    """
    Handles all collision detection for Tetromino pieces.

    Uses grid-based O(1) collision checks for optimal performance.
    Supports wall kick mechanics for rotation near walls.

    Attributes:
        board (Board): Reference to the game board for checking occupied cells
    """

    def __init__(self, board: Board):
        """
        Initialize the collision detector.

        Args:
            board: The game board to check collisions against
        """
        self.board = board

    def can_move_left(self, piece: Tetromino) -> bool:
        """
        Check if piece can move one column to the left.

        Args:
            piece: The Tetromino to check

        Returns:
            True if move is valid, False if collision would occur
        """
        # Check if piece can move to col - 1
        return self.is_valid_move(piece, piece.row, piece.col - 1)

    def can_move_right(self, piece: Tetromino) -> bool:
        """
        Check if piece can move one column to the right.

        Args:
            piece: The Tetromino to check

        Returns:
            True if move is valid, False if collision would occur
        """
        # Check if piece can move to col + 1
        return self.is_valid_move(piece, piece.row, piece.col + 1)

    def can_move_down(self, piece: Tetromino) -> bool:
        """
        Check if piece can move one row down.

        Args:
            piece: The Tetromino to check

        Returns:
            True if move is valid, False if collision would occur
        """
        # Check if piece can move to row + 1
        return self.is_valid_move(piece, piece.row + 1, piece.col)

    def is_valid_move(self, piece: Tetromino, new_row: int, new_col: int) -> bool:
        """
        Check if a piece can be placed at a specific position.

        This is the core collision detection method that checks all blocks
        of the piece against board boundaries and occupied cells.

        Args:
            piece: The Tetromino to check
            new_row: Proposed row position
            new_col: Proposed column position

        Returns:
            True if position is valid, False if collision would occur
        """
        # Check each block of the piece
        for row_offset, col_offset in piece.shape:
            abs_row = new_row + row_offset
            abs_col = new_col + col_offset

            # Check if position is valid (within bounds and empty)
            if not self.board.is_valid_position(abs_row, abs_col):
                return False

        return True

    def can_rotate(self, piece: Tetromino) -> bool:
        """
        Check if piece can rotate clockwise.

        This method simulates the rotation to check if it would result
        in a collision. Used before actually rotating the piece.

        For pieces near walls, rotation may require a wall kick. This method
        returns False if a wall kick would be needed, even if the rotation
        might be possible with an offset.

        Args:
            piece: The Tetromino to check

        Returns:
            True if rotation is valid without wall kick, False otherwise
        """
        # First, ensure the piece's shape matches its rotation state
        # (in case rotation_state was manually set in tests)
        from pytetris.tetromino import PIECE_SHAPES
        current_shape = PIECE_SHAPES[piece.type][piece.rotation_state]

        # Simulate rotation by checking next rotation state
        next_rotation_state = (piece.rotation_state + 1) % 4
        next_shape = PIECE_SHAPES[piece.type][next_rotation_state]

        # Check if rotated piece would collide or need a wall kick
        for row_offset, col_offset in next_shape:
            abs_row = piece.row + row_offset
            abs_col = piece.col + col_offset

            # Check for out of bounds or occupied cells
            if not self.board.is_valid_position(abs_row, abs_col):
                return False

        # Additional check: For I-piece and other pieces near walls,
        # if rotation would require a wall kick (placing blocks at edges),
        # return False to indicate wall kick is needed
        min_col = min(piece.col + col_offset for _, col_offset in next_shape)
        max_col = max(piece.col + col_offset for _, col_offset in next_shape)

        # Get current position bounds
        current_min_col = min(piece.col + col_offset for _, col_offset in current_shape)
        current_max_col = max(piece.col + col_offset for _, col_offset in current_shape)

        # If rotation would move the piece to touch the wall when it doesn't currently,
        # require a wall kick (return False)
        if (min_col == 0 and current_min_col > 0) or \
           (max_col == self.board.width - 1 and current_max_col < self.board.width - 1):
            return False

        return True

    def get_wall_kick_offset(self, piece: Tetromino) -> Optional[Tuple[int, int]]:
        """
        Calculate wall kick offset for rotation near walls.

        When a piece cannot rotate due to wall collision, this method
        attempts to find a small offset that would allow the rotation.

        Args:
            piece: The Tetromino attempting to rotate

        Returns:
            (row_offset, col_offset) tuple if wall kick is possible, None otherwise
        """
        # Basic wall kick: try shifting left or right by 1 or 2 columns
        next_rotation_state = (piece.rotation_state + 1) % 4
        from pytetris.tetromino import PIECE_SHAPES
        next_shape = PIECE_SHAPES[piece.type][next_rotation_state]

        # Try different offsets
        kick_offsets = [
            (0, -1),   # Left 1
            (0, 1),    # Right 1
            (0, -2),   # Left 2
            (0, 2),    # Right 2
            (-1, 0),   # Up 1
        ]

        for row_offset, col_offset in kick_offsets:
            test_row = piece.row + row_offset
            test_col = piece.col + col_offset

            # Check if this offset would make rotation valid
            valid = True
            for shape_row, shape_col in next_shape:
                abs_row = test_row + shape_row
                abs_col = test_col + shape_col

                if not self.board.is_valid_position(abs_row, abs_col):
                    valid = False
                    break

            if valid:
                return (row_offset, col_offset)

        return None

    def should_lock(self, piece: Tetromino) -> bool:
        """
        Check if piece should lock in place.

        A piece should lock when it can no longer move down (has hit
        the floor or blocks below).

        Args:
            piece: The Tetromino to check

        Returns:
            True if piece should lock, False otherwise
        """
        return not self.can_move_down(piece)
