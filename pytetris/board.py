"""
Game board module for PyTetris.

This module implements the game board logic including:
- Board initialization and state management
- Cell operations (set, get, clear)
- Boundary validation
- Line detection and clearing
- Game over detection

Related PRD Requirements: REQ-1 (Game Board and Pieces), REQ-4 (Line Clearing)
"""

from typing import List, Optional


class Board:
    """
    Represents the Tetris game board.

    The board is a 10x20 grid where pieces are placed. Cells can either be
    empty (None) or contain a color value representing a placed block.

    Attributes:
        width (int): Number of columns (10 for standard Tetris)
        height (int): Number of rows (20 for standard Tetris)
        grid (List[List[Optional[str]]]): 2D array storing cell states
    """

    def __init__(self, width: int = 10, height: int = 20):
        """
        Initialize a new game board.

        Args:
            width: Number of columns (default: 10)
            height: Number of rows (default: 20)
        """
        self.width = width
        self.height = height
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]

    def set_cell(self, row: int, col: int, value: str) -> None:
        """
        Set a cell to a specific value.

        Args:
            row: Row index (0 = top)
            col: Column index (0 = left)
            value: Color value to set (e.g., 'cyan', 'red')
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = value

    def get_cell(self, row: int, col: int) -> Optional[str]:
        """
        Get the value of a cell.

        Args:
            row: Row index
            col: Column index

        Returns:
            Cell value (color string) or None if empty
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None

    def clear_cell(self, row: int, col: int) -> None:
        """
        Clear a cell (set to None).

        Args:
            row: Row index
            col: Column index
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = None

    def is_empty(self, row: int, col: int) -> bool:
        """
        Check if a cell is empty.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if cell is empty (None), False otherwise
        """
        return self.get_cell(row, col) is None

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if a position is valid (within bounds and empty).

        This method checks both boundary conditions and whether the cell
        is occupied. Used for collision detection.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if position is within bounds and empty, False otherwise
        """
        # Check boundaries
        if row < 0 or row >= self.height:
            return False
        if col < 0 or col >= self.width:
            return False

        # Check if cell is empty
        return self.is_empty(row, col)

    def get_complete_lines(self) -> List[int]:
        """
        Detect completed horizontal lines.

        A line is complete when all 10 columns are filled (non-None).
        Related to REQ-4: Line Clearing.

        Returns:
            List of row indices that are complete
        """
        complete_lines = []
        for row in range(self.height):
            if all(self.grid[row][col] is not None for col in range(self.width)):
                complete_lines.append(row)
        return complete_lines

    def clear_lines(self, lines: List[int]) -> None:
        """
        Clear specified lines and move blocks above downward.

        This implements the core line-clearing mechanic. When lines are
        cleared, all blocks above the cleared lines fall down to fill
        the gaps.

        Related to REQ-4: Line Clearing.

        Args:
            lines: List of row indices to clear (sorted or unsorted)
        """
        if not lines:
            return

        # Sort lines in descending order to process from bottom to top
        sorted_lines = sorted(lines, reverse=True)

        # Remove each complete line
        for line in sorted_lines:
            del self.grid[line]

        # Add new empty lines at the top
        num_lines_cleared = len(lines)
        for _ in range(num_lines_cleared):
            self.grid.insert(0, [None for _ in range(self.width)])

    def is_game_over(self) -> bool:
        """
        Check if game over condition is met.

        Game over occurs when blocks are present in the spawn area
        (typically the top rows where new pieces spawn).

        Returns:
            True if blocks are present at the top, False otherwise
        """
        # Check top row for any blocks (spawn area)
        for col in range(self.width):
            if not self.is_empty(0, col):
                return True
        return False

    def reset(self) -> None:
        """
        Reset the board to initial empty state.

        Clears all cells, making the board ready for a new game.
        """
        self.grid = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
