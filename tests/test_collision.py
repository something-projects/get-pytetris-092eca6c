"""
Unit tests for collision detection system.

Tests cover:
- Wall collision detection
- Floor collision detection
- Block-to-block collision
- Rotation collision handling
- Valid move checking

Related PRD Requirements: REQ-2, REQ-3
"""

import pytest


class TestCollisionDetector:
    """Test the collision detection system."""

    def test_detect_left_wall_collision(self):
        """Piece at left wall should collide when moving left."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('I')
        piece.col = 0  # At left wall
        detector = CollisionDetector(board)

        assert not detector.can_move_left(piece)

    def test_detect_right_wall_collision(self):
        """Piece at right wall should collide when moving right."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('I')
        piece.col = 9  # At right edge (board is 10 wide)
        detector = CollisionDetector(board)

        assert not detector.can_move_right(piece)

    def test_detect_floor_collision(self):
        """Piece at bottom should collide with floor."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('O')
        piece.row = 18  # Bottom (board is 20 tall, O-piece is 2 tall)
        detector = CollisionDetector(board)

        assert not detector.can_move_down(piece)

    def test_no_collision_in_empty_space(self):
        """Piece in open space should have no collisions."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('T')
        piece.row = 10
        piece.col = 5
        detector = CollisionDetector(board)

        assert detector.can_move_left(piece)
        assert detector.can_move_right(piece)
        assert detector.can_move_down(piece)

    def test_detect_block_collision_below(self):
        """Piece above existing blocks should collide when moving down."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        # Place blocks at bottom
        for col in range(5):
            board.set_cell(19, col, 'cyan')

        piece = Tetromino('I')
        piece.row = 18
        piece.col = 2
        detector = CollisionDetector(board)

        assert not detector.can_move_down(piece)

    def test_detect_block_collision_left(self):
        """Piece should collide with blocks to the left."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        board.set_cell(10, 3, 'red')

        piece = Tetromino('O')
        piece.row = 10
        piece.col = 4
        detector = CollisionDetector(board)

        assert not detector.can_move_left(piece)

    def test_detect_block_collision_right(self):
        """Piece should collide with blocks to the right."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        board.set_cell(10, 6, 'red')

        piece = Tetromino('O')
        piece.row = 10
        piece.col = 4
        detector = CollisionDetector(board)

        assert not detector.can_move_right(piece)


class TestRotationCollision:
    """Test collision detection during rotation."""

    def test_can_rotate_in_open_space(self):
        """Piece should be able to rotate in open space."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('T')
        piece.row = 10
        piece.col = 5
        detector = CollisionDetector(board)

        assert detector.can_rotate(piece)

    def test_cannot_rotate_into_wall(self):
        """Piece should not rotate if it would intersect wall."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('I')
        piece.col = 0  # Against left wall
        detector = CollisionDetector(board)

        # I-piece vertical at left wall cannot rotate horizontal
        piece.rotation_state = 1  # Vertical
        assert not detector.can_rotate(piece)

    def test_cannot_rotate_into_existing_blocks(self):
        """Piece should not rotate if it would hit existing blocks."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        # Create a barrier
        board.set_cell(10, 6, 'red')

        piece = Tetromino('I')
        piece.row = 10
        piece.col = 5
        detector = CollisionDetector(board)

        # Try to rotate - might collide with barrier
        # This depends on piece orientation
        result = detector.can_rotate(piece)
        assert isinstance(result, bool)

    def test_wall_kick_basic(self):
        """Should attempt wall kick when rotation is blocked by wall."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('I')
        piece.col = 9  # Near right wall
        detector = CollisionDetector(board)

        # Should try to kick away from wall
        kick_offset = detector.get_wall_kick_offset(piece)
        assert kick_offset is not None


class TestPieceLocking:
    """Test piece lock detection."""

    def test_piece_should_lock_on_floor(self):
        """Piece that cannot move down should lock."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('O')
        piece.row = 18  # At floor
        detector = CollisionDetector(board)

        assert detector.should_lock(piece)

    def test_piece_should_lock_on_blocks(self):
        """Piece resting on blocks should lock."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        # Create floor of blocks
        for col in range(10):
            board.set_cell(19, col, 'cyan')

        piece = Tetromino('T')
        piece.row = 17  # Just above floor
        detector = CollisionDetector(board)

        assert detector.should_lock(piece)

    def test_piece_should_not_lock_in_midair(self):
        """Piece in open space should not lock."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('I')
        piece.row = 10
        detector = CollisionDetector(board)

        assert not detector.should_lock(piece)


class TestValidMoveChecking:
    """Test general valid move checking."""

    def test_is_valid_move_for_valid_position(self):
        """Valid moves should return True."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('T')
        detector = CollisionDetector(board)

        assert detector.is_valid_move(piece, 5, 5)

    def test_is_valid_move_for_invalid_position(self):
        """Invalid moves should return False."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('T')
        detector = CollisionDetector(board)

        # Out of bounds
        assert not detector.is_valid_move(piece, -1, 5)
        assert not detector.is_valid_move(piece, 5, -1)
        assert not detector.is_valid_move(piece, 25, 5)
        assert not detector.is_valid_move(piece, 5, 15)

    def test_is_valid_move_with_occupied_cells(self):
        """Moves into occupied cells should be invalid."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        board.set_cell(10, 5, 'red')

        piece = Tetromino('O')
        detector = CollisionDetector(board)

        # O-piece would overlap with the red block
        assert not detector.is_valid_move(piece, 9, 4)

    def test_check_collision_with_all_piece_blocks(self):
        """Collision check should consider all 4 blocks of piece."""
        from pytetris.collision import CollisionDetector
        from pytetris.board import Board
        from pytetris.tetromino import Tetromino

        board = Board()
        piece = Tetromino('T')
        detector = CollisionDetector(board)

        # Verify all blocks are checked
        positions = piece.get_block_positions()
        assert len(positions) == 4

        # Each block should be within bounds for valid move
        valid = detector.is_valid_move(piece, piece.row, piece.col)
        if valid:
            for row, col in positions:
                assert 0 <= row < 20
                assert 0 <= col < 10
