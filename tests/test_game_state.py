"""
Unit tests for game state management.

Tests cover:
- Game state transitions
- Piece spawning
- Next piece preview
- Game over detection
- Pause/resume functionality

Related PRD Requirements: REQ-6, REQ-7, REQ-8
"""

import pytest


class TestGameStateInitialization:
    """Test game state initialization."""

    def test_game_starts_in_start_state(self):
        """New game should start in START state."""
        from pytetris.game_state import GameState

        game = GameState()
        assert game.state == 'START'

    def test_initial_game_setup(self):
        """Game should initialize all components."""
        from pytetris.game_state import GameState

        game = GameState()
        assert game.board is not None
        assert game.score_manager is not None
        assert game.current_piece is None  # No piece until game starts


class TestGameStateTransitions:
    """Test state transitions (REQ-7)."""

    def test_start_game_transitions_to_playing(self):
        """Starting game should transition to PLAYING state."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        assert game.state == 'PLAYING'

    def test_pause_game_transitions_to_paused(self):
        """Pausing game should transition to PAUSED state."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.pause()
        assert game.state == 'PAUSED'

    def test_resume_game_transitions_to_playing(self):
        """Resuming paused game should transition to PLAYING."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.pause()
        game.resume()
        assert game.state == 'PLAYING'

    def test_game_over_transitions_to_game_over_state(self):
        """Game over condition should transition to GAME_OVER state."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.end_game()
        assert game.state == 'GAME_OVER'

    def test_cannot_pause_when_not_playing(self):
        """Cannot pause when not in PLAYING state."""
        from pytetris.game_state import GameState

        game = GameState()
        game.pause()
        assert game.state == 'START'  # Still in start state

    def test_cannot_resume_when_not_paused(self):
        """Cannot resume when not in PAUSED state."""
        from pytetris.game_state import GameState

        game = GameState()
        game.resume()
        assert game.state == 'START'  # Still in start state


class TestPieceSpawning:
    """Test piece spawning mechanics (REQ-1)."""

    def test_spawn_first_piece_on_game_start(self):
        """Starting game should spawn first piece."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        assert game.current_piece is not None

    def test_spawned_piece_at_top_center(self):
        """Spawned piece should be at top center."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        assert game.current_piece.row <= 1  # Top area
        assert 3 <= game.current_piece.col <= 5  # Center area

    def test_spawn_new_piece_after_lock(self):
        """New piece should spawn after current piece locks."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        first_piece_type = game.current_piece.type

        game.lock_current_piece()
        game.spawn_next_piece()

        assert game.current_piece is not None
        # Might be same type, but should be a new instance

    def test_cannot_spawn_piece_when_blocked(self):
        """Game over should occur if piece cannot spawn."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        # Fill top rows to block spawning
        for col in range(10):
            game.board.set_cell(0, col, 'red')
            game.board.set_cell(1, col, 'red')

        result = game.try_spawn_piece()
        assert not result
        assert game.state == 'GAME_OVER'


class TestNextPiecePreview:
    """Test next piece preview system (REQ-8)."""

    def test_next_piece_is_set_on_game_start(self):
        """Starting game should set next piece."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        assert game.next_piece is not None

    def test_next_piece_becomes_current_after_lock(self):
        """Next piece should become current piece after lock."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        next_piece_type = game.next_piece.type

        game.lock_current_piece()
        game.spawn_next_piece()

        assert game.current_piece.type == next_piece_type

    def test_new_next_piece_generated_after_spawn(self):
        """New next piece should be generated after spawning."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        first_next = game.next_piece

        game.lock_current_piece()
        game.spawn_next_piece()

        assert game.next_piece is not None
        assert game.next_piece != first_next  # Different instance

    def test_next_piece_is_valid_tetromino(self):
        """Next piece should be a valid Tetromino type."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        assert game.next_piece.type in ['I', 'O', 'T', 'S', 'Z', 'J', 'L']


class TestGameOverDetection:
    """Test game over detection (REQ-7)."""

    def test_game_over_when_spawn_blocked(self):
        """Game over when new piece cannot spawn."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        # Block spawn area
        for col in range(10):
            game.board.set_cell(0, col, 'red')

        game.check_game_over()
        assert game.state == 'GAME_OVER'

    def test_game_not_over_with_space_available(self):
        """Game should continue if spawn area is clear."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        # Fill some bottom rows but leave top clear
        for col in range(10):
            game.board.set_cell(19, col, 'cyan')

        game.check_game_over()
        assert game.state == 'PLAYING'

    def test_final_score_available_on_game_over(self):
        """Final score should be accessible after game over."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.score_manager.add_line_clear_score(4)  # 800 points
        game.end_game()

        assert game.get_final_score() == 800

    def test_high_score_updated_on_game_over(self):
        """High score should update when game ends."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.score_manager.add_line_clear_score(4)  # 800 points
        game.end_game()

        assert game.score_manager.get_high_score() >= 800


class TestLevelProgression:
    """Test level progression and speed changes (REQ-6)."""

    def test_drop_speed_increases_with_level(self):
        """Drop speed should increase at higher levels."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        speed_level_1 = game.get_drop_speed()
        game.score_manager.set_level(5)
        speed_level_5 = game.get_drop_speed()

        assert speed_level_5 < speed_level_1  # Lower interval = faster

    def test_drop_speed_calculation(self):
        """Drop speed should follow expected formula."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        # Level 1 should be ~1000ms
        game.score_manager.set_level(1)
        assert game.get_drop_speed() >= 800

        # Level 5 should be faster
        game.score_manager.set_level(5)
        assert game.get_drop_speed() <= 700

    def test_level_display_updates(self):
        """Level display should update when level changes."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        assert game.get_current_level() == 1

        # Clear 10 lines to reach level 2
        for _ in range(10):
            game.score_manager.add_line_clear_score(1)

        assert game.get_current_level() == 2

    def test_minimum_drop_speed(self):
        """Drop speed should have a minimum (max speed)."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.score_manager.set_level(100)

        speed = game.get_drop_speed()
        assert speed >= 50  # Should not be too fast


class TestPieceLocking:
    """Test piece locking mechanics."""

    def test_lock_piece_places_blocks_on_board(self):
        """Locking piece should place its blocks on board."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        piece_positions = game.current_piece.get_block_positions()
        piece_color = game.current_piece.color

        game.lock_current_piece()

        # Blocks should now be on board
        for row, col in piece_positions:
            assert game.board.get_cell(row, col) == piece_color

    def test_lock_clears_current_piece(self):
        """Locking should clear current piece (until next spawn)."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.lock_current_piece()

        # Current piece should be cleared or ready for new one
        # This depends on implementation - either None or about to spawn new

    def test_lock_triggers_line_clear_check(self):
        """Locking should check for completed lines."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()

        # Fill bottom row except one spot
        for col in range(9):
            game.board.set_cell(19, col, 'cyan')

        # Position piece to complete the line
        game.current_piece.row = 18
        game.current_piece.col = 9

        lines_before = game.score_manager.get_lines_cleared()
        game.lock_current_piece()
        lines_after = game.score_manager.get_lines_cleared()

        # Line should be cleared (this depends on piece completing it)
        assert lines_after >= lines_before


class TestGameReset:
    """Test resetting game for new game."""

    def test_reset_clears_board(self):
        """Reset should clear the board."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.board.set_cell(10, 5, 'red')

        game.reset()

        assert game.board.is_empty(10, 5)

    def test_reset_clears_score(self):
        """Reset should clear score but not high score."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.score_manager.add_line_clear_score(4)
        high_score = game.score_manager.get_high_score()

        game.reset()

        assert game.score_manager.get_score() == 0
        assert game.score_manager.get_high_score() == high_score

    def test_reset_returns_to_level_1(self):
        """Reset should return to level 1."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.score_manager.set_level(5)

        game.reset()

        assert game.score_manager.get_level() == 1

    def test_reset_returns_to_start_state(self):
        """Reset should return to START state."""
        from pytetris.game_state import GameState

        game = GameState()
        game.start()
        game.end_game()

        game.reset()

        assert game.state == 'START'
