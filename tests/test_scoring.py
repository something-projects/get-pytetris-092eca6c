"""
Unit tests for scoring system and line clearing.

Tests cover:
- Score calculation for line clears
- Soft drop scoring
- Level-based score multipliers
- High score tracking
- Lines cleared counter

Related PRD Requirements: REQ-4, REQ-5, REQ-10
"""

import pytest


class TestScoreInitialization:
    """Test score manager initialization."""

    def test_score_starts_at_zero(self):
        """New game should start with 0 score."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        assert score_mgr.get_score() == 0

    def test_lines_cleared_starts_at_zero(self):
        """New game should start with 0 lines cleared."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        assert score_mgr.get_lines_cleared() == 0

    def test_level_starts_at_one(self):
        """New game should start at level 1."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        assert score_mgr.get_level() == 1


class TestSingleLineScoring:
    """Test scoring for single line clears (REQ-5)."""

    def test_single_line_score_at_level_1(self):
        """Single line at level 1 should award 100 points."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(1)
        assert score_mgr.get_score() == 100

    def test_single_line_score_at_level_2(self):
        """Single line at level 2 should award 200 points (100 × 2)."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.set_level(2)
        score_mgr.add_line_clear_score(1)
        assert score_mgr.get_score() == 200

    def test_single_line_score_at_level_5(self):
        """Single line at level 5 should award 500 points (100 × 5)."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.set_level(5)
        score_mgr.add_line_clear_score(1)
        assert score_mgr.get_score() == 500


class TestMultipleLineScoring:
    """Test scoring for multiple line clears."""

    def test_double_line_score_at_level_1(self):
        """Double line at level 1 should award 300 points."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(2)
        assert score_mgr.get_score() == 300

    def test_triple_line_score_at_level_1(self):
        """Triple line at level 1 should award 500 points."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(3)
        assert score_mgr.get_score() == 500

    def test_tetris_score_at_level_1(self):
        """Tetris (4 lines) at level 1 should award 800 points."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(4)
        assert score_mgr.get_score() == 800

    def test_double_line_score_at_level_3(self):
        """Double line at level 3 should award 900 points (300 × 3)."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.set_level(3)
        score_mgr.add_line_clear_score(2)
        assert score_mgr.get_score() == 900

    def test_tetris_score_at_level_4(self):
        """Tetris at level 4 should award 3200 points (800 × 4)."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.set_level(4)
        score_mgr.add_line_clear_score(4)
        assert score_mgr.get_score() == 3200


class TestSoftDropScoring:
    """Test soft drop scoring (REQ-5)."""

    def test_soft_drop_awards_one_point_per_cell(self):
        """Each cell descended should award 1 point."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_soft_drop_score(5)
        assert score_mgr.get_score() == 5

    def test_soft_drop_score_accumulates(self):
        """Multiple soft drops should accumulate."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_soft_drop_score(3)
        score_mgr.add_soft_drop_score(7)
        assert score_mgr.get_score() == 10

    def test_soft_drop_combines_with_line_clear(self):
        """Soft drop and line clear scores should combine."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_soft_drop_score(10)
        score_mgr.add_line_clear_score(1)
        assert score_mgr.get_score() == 110  # 10 + 100


class TestLinesCleared:
    """Test lines cleared counter."""

    def test_lines_cleared_increments(self):
        """Lines cleared should increment correctly."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(1)
        assert score_mgr.get_lines_cleared() == 1

    def test_multiple_lines_cleared_at_once(self):
        """Clearing multiple lines should increment counter correctly."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(4)
        assert score_mgr.get_lines_cleared() == 4

    def test_cumulative_lines_cleared(self):
        """Lines cleared should accumulate over multiple clears."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(1)
        score_mgr.add_line_clear_score(2)
        score_mgr.add_line_clear_score(3)
        assert score_mgr.get_lines_cleared() == 6


class TestLevelProgression:
    """Test level progression based on lines cleared (REQ-6)."""

    def test_level_increases_after_10_lines(self):
        """Level should increase after clearing 10 lines."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        # Clear 10 lines
        for _ in range(10):
            score_mgr.add_line_clear_score(1)

        assert score_mgr.get_level() == 2

    def test_level_increases_after_20_lines(self):
        """Level should be 3 after clearing 20 lines."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        # Clear 20 lines
        for _ in range(20):
            score_mgr.add_line_clear_score(1)

        assert score_mgr.get_level() == 3

    def test_level_calculation_formula(self):
        """Level should be calculated as 1 + (lines_cleared // 10)."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()

        test_cases = [
            (0, 1),   # 0 lines = level 1
            (5, 1),   # 5 lines = level 1
            (9, 1),   # 9 lines = level 1
            (10, 2),  # 10 lines = level 2
            (15, 2),  # 15 lines = level 2
            (19, 2),  # 19 lines = level 2
            (20, 3),  # 20 lines = level 3
            (50, 6),  # 50 lines = level 6
            (99, 10), # 99 lines = level 10
        ]

        for lines, expected_level in test_cases:
            score_mgr = ScoreManager()
            for _ in range(lines):
                score_mgr.add_line_clear_score(1)
            assert score_mgr.get_level() == expected_level


class TestHighScore:
    """Test high score tracking (REQ-10)."""

    def test_high_score_starts_at_zero(self):
        """High score should start at 0."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        assert score_mgr.get_high_score() == 0

    def test_high_score_updates_when_exceeded(self):
        """High score should update when current score exceeds it."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(4)  # 800 points

        score_mgr.update_high_score()
        assert score_mgr.get_high_score() == 800

    def test_high_score_persists_across_games(self):
        """High score should be maintained when starting new game."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(4)  # 800 points
        score_mgr.update_high_score()

        # Reset for new game
        score_mgr.reset()
        assert score_mgr.get_score() == 0
        assert score_mgr.get_high_score() == 800

    def test_high_score_does_not_decrease(self):
        """High score should never decrease."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager()
        score_mgr.add_line_clear_score(4)  # 800 points
        score_mgr.update_high_score()

        score_mgr.reset()
        score_mgr.add_line_clear_score(1)  # 100 points
        score_mgr.update_high_score()

        assert score_mgr.get_high_score() == 800  # Still 800, not 100


class TestScorePersistence:
    """Test score persistence to file (REQ-10)."""

    def test_save_high_score_to_file(self):
        """High score should be saved to file."""
        from pytetris.score_manager import ScoreManager
        import os
        import tempfile

        # Use temp file for testing
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()

        try:
            score_mgr = ScoreManager(save_file=temp_file.name)
            score_mgr.add_line_clear_score(4)
            score_mgr.update_high_score()
            score_mgr.save()

            assert os.path.exists(temp_file.name)
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_load_high_score_from_file(self):
        """High score should be loaded from file."""
        from pytetris.score_manager import ScoreManager
        import os
        import tempfile

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()

        try:
            # Save high score
            score_mgr1 = ScoreManager(save_file=temp_file.name)
            score_mgr1.add_line_clear_score(4)
            score_mgr1.update_high_score()
            score_mgr1.save()

            # Load high score
            score_mgr2 = ScoreManager(save_file=temp_file.name)
            score_mgr2.load()

            assert score_mgr2.get_high_score() == 800
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_handle_missing_save_file_gracefully(self):
        """Should handle missing save file without crashing."""
        from pytetris.score_manager import ScoreManager

        score_mgr = ScoreManager(save_file='/nonexistent/path/scores.json')
        score_mgr.load()  # Should not crash

        assert score_mgr.get_high_score() == 0  # Default value
