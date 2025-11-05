"""
Unit tests for the game board module.

Tests cover:
- Board initialization
- Cell state management
- Boundary checking
- Board state queries

Related PRD Requirements: REQ-1 (Game Board and Pieces)
"""

import pytest


class TestBoardInitialization:
    """Test board creation and initialization."""

    def test_board_creates_with_correct_dimensions(self):
        """Board should be 10 columns by 20 rows (REQ-1)."""
        from pytetris.board import Board

        board = Board()
        assert board.width == 10
        assert board.height == 20

    def test_board_initializes_empty(self):
        """New board should have all cells empty."""
        from pytetris.board import Board

        board = Board()
        for row in range(board.height):
            for col in range(board.width):
                assert board.is_empty(row, col)

    def test_board_grid_structure(self):
        """Board should maintain a 2D grid structure."""
        from pytetris.board import Board

        board = Board()
        assert hasattr(board, 'grid')
        assert len(board.grid) == 20  # 20 rows
        assert all(len(row) == 10 for row in board.grid)  # 10 columns each


class TestBoardCellOperations:
    """Test individual cell operations."""

    def test_set_cell_value(self):
        """Should be able to set a cell to a specific value."""
        from pytetris.board import Board

        board = Board()
        board.set_cell(5, 3, 'cyan')
        assert board.get_cell(5, 3) == 'cyan'

    def test_clear_cell(self):
        """Should be able to clear a cell."""
        from pytetris.board import Board

        board = Board()
        board.set_cell(5, 3, 'cyan')
        board.clear_cell(5, 3)
        assert board.is_empty(5, 3)

    def test_get_cell_returns_none_for_empty(self):
        """Empty cells should return None."""
        from pytetris.board import Board

        board = Board()
        assert board.get_cell(0, 0) is None


class TestBoardBoundaryChecking:
    """Test boundary validation."""

    def test_is_valid_position_within_bounds(self):
        """Valid positions should return True."""
        from pytetris.board import Board

        board = Board()
        assert board.is_valid_position(0, 0)
        assert board.is_valid_position(19, 9)
        assert board.is_valid_position(10, 5)

    def test_is_valid_position_out_of_bounds(self):
        """Out of bounds positions should return False."""
        from pytetris.board import Board

        board = Board()
        assert not board.is_valid_position(-1, 0)
        assert not board.is_valid_position(0, -1)
        assert not board.is_valid_position(20, 0)
        assert not board.is_valid_position(0, 10)

    def test_is_valid_position_with_occupied_cell(self):
        """Occupied cells should return False."""
        from pytetris.board import Board

        board = Board()
        board.set_cell(5, 5, 'red')
        assert not board.is_valid_position(5, 5)


class TestBoardLineClearing:
    """Test line detection and clearing (REQ-4)."""

    def test_detect_no_complete_lines_on_empty_board(self):
        """Empty board should have no complete lines."""
        from pytetris.board import Board

        board = Board()
        complete_lines = board.get_complete_lines()
        assert len(complete_lines) == 0

    def test_detect_single_complete_line(self):
        """Should detect a single complete line."""
        from pytetris.board import Board

        board = Board()
        # Fill row 19 (bottom row)
        for col in range(10):
            board.set_cell(19, col, 'cyan')

        complete_lines = board.get_complete_lines()
        assert len(complete_lines) == 1
        assert 19 in complete_lines

    def test_detect_multiple_complete_lines(self):
        """Should detect multiple complete lines."""
        from pytetris.board import Board

        board = Board()
        # Fill rows 18 and 19
        for row in [18, 19]:
            for col in range(10):
                board.set_cell(row, col, 'cyan')

        complete_lines = board.get_complete_lines()
        assert len(complete_lines) == 2
        assert 18 in complete_lines
        assert 19 in complete_lines

    def test_clear_single_line(self):
        """Clearing a line should remove it and move blocks down."""
        from pytetris.board import Board

        board = Board()
        # Fill row 19
        for col in range(10):
            board.set_cell(19, col, 'cyan')
        # Place a block above
        board.set_cell(18, 5, 'red')

        board.clear_lines([19])

        # Row 19 should now have the red block
        assert board.get_cell(19, 5) == 'red'
        # Other cells in row 19 should be empty
        assert board.is_empty(19, 0)

    def test_clear_multiple_lines(self):
        """Clearing multiple lines should move all blocks above down correctly."""
        from pytetris.board import Board

        board = Board()
        # Fill rows 18, 19
        for row in [18, 19]:
            for col in range(10):
                board.set_cell(row, col, 'cyan')
        # Place a block above
        board.set_cell(17, 3, 'purple')

        board.clear_lines([18, 19])

        # The purple block should now be at row 19
        assert board.get_cell(19, 3) == 'purple'


class TestBoardState:
    """Test board state queries."""

    def test_is_game_over_empty_board(self):
        """Empty board should not be game over."""
        from pytetris.board import Board

        board = Board()
        assert not board.is_game_over()

    def test_is_game_over_with_blocks_at_top(self):
        """Blocks in spawn area (top rows) should trigger game over."""
        from pytetris.board import Board

        board = Board()
        board.set_cell(0, 4, 'red')  # Block at top center
        assert board.is_game_over()

    def test_reset_board(self):
        """Reset should clear all cells."""
        from pytetris.board import Board

        board = Board()
        # Add some blocks
        board.set_cell(5, 5, 'cyan')
        board.set_cell(10, 3, 'red')

        board.reset()

        # All cells should be empty
        for row in range(board.height):
            for col in range(board.width):
                assert board.is_empty(row, col)
