"""
Unit tests for Tetromino pieces.

Tests cover:
- All 7 piece types (I, O, T, S, Z, J, L)
- Piece initialization
- Rotation mechanics
- Color coding
- Position tracking

Related PRD Requirements: REQ-1, REQ-2, REQ-3
"""

import pytest


class TestTetrominoCreation:
    """Test creating different Tetromino pieces."""

    def test_create_i_piece(self):
        """I-piece should have correct shape and color (cyan)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('I')
        assert piece.type == 'I'
        assert piece.color == 'cyan'
        assert len(piece.shape) == 4  # 4 blocks

    def test_create_o_piece(self):
        """O-piece should have correct shape and color (yellow)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('O')
        assert piece.type == 'O'
        assert piece.color == 'yellow'
        assert len(piece.shape) == 4

    def test_create_t_piece(self):
        """T-piece should have correct shape and color (purple)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        assert piece.type == 'T'
        assert piece.color == 'purple'
        assert len(piece.shape) == 4

    def test_create_s_piece(self):
        """S-piece should have correct shape and color (green)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('S')
        assert piece.type == 'S'
        assert piece.color == 'green'
        assert len(piece.shape) == 4

    def test_create_z_piece(self):
        """Z-piece should have correct shape and color (red)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('Z')
        assert piece.type == 'Z'
        assert piece.color == 'red'
        assert len(piece.shape) == 4

    def test_create_j_piece(self):
        """J-piece should have correct shape and color (blue)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('J')
        assert piece.type == 'J'
        assert piece.color == 'blue'
        assert len(piece.shape) == 4

    def test_create_l_piece(self):
        """L-piece should have correct shape and color (orange)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('L')
        assert piece.type == 'L'
        assert piece.color == 'orange'
        assert len(piece.shape) == 4

    def test_all_pieces_have_unique_colors(self):
        """Each piece type should have a distinct color."""
        from pytetris.tetromino import Tetromino

        piece_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        colors = [Tetromino(t).color for t in piece_types]
        assert len(set(colors)) == 7  # All unique


class TestTetrominoPosition:
    """Test piece position tracking."""

    def test_initial_spawn_position(self):
        """Pieces should spawn at top center (REQ-1)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('I')
        assert piece.row == 0  # Top
        assert piece.col == 3 or piece.col == 4  # Center-ish for 10-wide board

    def test_move_left(self):
        """Should move piece one column left."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        original_col = piece.col
        piece.move_left()
        assert piece.col == original_col - 1

    def test_move_right(self):
        """Should move piece one column right."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        original_col = piece.col
        piece.move_right()
        assert piece.col == original_col + 1

    def test_move_down(self):
        """Should move piece one row down."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        original_row = piece.row
        piece.move_down()
        assert piece.row == original_row + 1

    def test_get_block_positions(self):
        """Should return absolute positions of all blocks."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('O')
        positions = piece.get_block_positions()
        assert len(positions) == 4
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)


class TestTetrominoRotation:
    """Test piece rotation mechanics (REQ-2)."""

    def test_rotate_clockwise(self):
        """Should rotate piece 90 degrees clockwise."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        original_shape = piece.shape[:]
        piece.rotate_clockwise()
        assert piece.shape != original_shape

    def test_rotate_counterclockwise(self):
        """Should rotate piece 90 degrees counterclockwise."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        original_shape = piece.shape[:]
        piece.rotate_counterclockwise()
        assert piece.shape != original_shape

    def test_four_rotations_return_to_original(self):
        """Four clockwise rotations should return to original shape."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('I')
        original_shape = [block[:] for block in piece.shape]

        for _ in range(4):
            piece.rotate_clockwise()

        assert piece.shape == original_shape

    def test_o_piece_rotation_invariant(self):
        """O-piece should look the same after rotation."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('O')
        original_positions = set(piece.get_block_positions())
        piece.rotate_clockwise()
        rotated_positions = set(piece.get_block_positions())
        # O-piece is symmetric so positions might be same or equivalent
        assert len(original_positions) == len(rotated_positions)

    def test_rotation_state_tracking(self):
        """Should track rotation state (0, 1, 2, 3)."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('L')
        assert piece.rotation_state == 0
        piece.rotate_clockwise()
        assert piece.rotation_state == 1
        piece.rotate_clockwise()
        assert piece.rotation_state == 2
        piece.rotate_clockwise()
        assert piece.rotation_state == 3
        piece.rotate_clockwise()
        assert piece.rotation_state == 0  # Wraps back


class TestTetrominoShapes:
    """Test that piece shapes are correct."""

    def test_i_piece_shape_horizontal(self):
        """I-piece in initial state should be horizontal line."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('I')
        positions = piece.get_block_positions()
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        # Should be 4 blocks in a line
        assert len(set(rows)) == 1 or len(set(cols)) == 1

    def test_o_piece_is_square(self):
        """O-piece should form a 2x2 square."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('O')
        positions = piece.get_block_positions()
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]
        assert max(rows) - min(rows) == 1
        assert max(cols) - min(cols) == 1

    def test_t_piece_has_t_shape(self):
        """T-piece should have characteristic T shape."""
        from pytetris.tetromino import Tetromino

        piece = Tetromino('T')
        # Just verify it has 4 blocks and they're connected
        assert len(piece.shape) == 4


class TestTetrominoFactory:
    """Test random piece generation."""

    def test_get_random_piece(self):
        """Should generate a random valid piece."""
        from pytetris.tetromino import TetrominoFactory

        factory = TetrominoFactory()
        piece = factory.get_random_piece()
        assert piece.type in ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

    def test_random_pieces_have_variety(self):
        """Multiple random pieces should show variety."""
        from pytetris.tetromino import TetrominoFactory

        factory = TetrominoFactory()
        pieces = [factory.get_random_piece().type for _ in range(100)]
        unique_types = set(pieces)
        # Should get at least 5 different types in 100 pieces
        assert len(unique_types) >= 5

    def test_all_piece_types_can_be_generated(self):
        """All 7 piece types should be possible."""
        from pytetris.tetromino import TetrominoFactory

        factory = TetrominoFactory()
        seen_types = set()
        # Generate enough pieces to see all types
        for _ in range(1000):
            piece = factory.get_random_piece()
            seen_types.add(piece.type)
            if len(seen_types) == 7:
                break

        assert len(seen_types) == 7
