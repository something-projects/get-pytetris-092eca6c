"""
Game state management module for PyTetris.

This module implements the complete game lifecycle including:
- State transitions (START, PLAYING, PAUSED, GAME_OVER)
- Piece spawning and management
- Next piece preview system
- Game over detection
- Drop speed calculation based on level
- Piece locking and line clearing

Related PRD Requirements: REQ-6 (Level Progression), REQ-7 (Game States), REQ-8 (Preview)
"""

from typing import Optional
from pytetris.board import Board
from pytetris.score_manager import ScoreManager
from pytetris.tetromino import Tetromino, TetrominoFactory
from pytetris.collision import CollisionDetector


class GameState:
    """
    Manages the complete game lifecycle and state.

    Handles state transitions, piece management, scoring integration,
    and game progression. Coordinates between Board, ScoreManager,
    and piece logic.

    States:
    - START: Initial state before game begins
    - PLAYING: Active gameplay
    - PAUSED: Game paused by player
    - GAME_OVER: Game ended, pieces can no longer spawn

    Attributes:
        state (str): Current game state
        board (Board): Game board instance
        score_manager (ScoreManager): Score tracking instance
        current_piece (Optional[Tetromino]): Currently active piece
        next_piece (Optional[Tetromino]): Preview of next piece
        collision_detector (CollisionDetector): Collision detection instance
        piece_factory (TetrominoFactory): Factory for generating pieces
    """

    def __init__(self):
        """Initialize the game state."""
        self.state = 'START'
        self.board = Board()
        self.score_manager = ScoreManager()
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.collision_detector = CollisionDetector(self.board)
        self.piece_factory = TetrominoFactory()

    def start(self) -> None:
        """
        Start a new game.

        Transitions to PLAYING state and spawns the first piece.
        """
        if self.state == 'START':
            self.state = 'PLAYING'
            # Generate next piece for preview
            self.next_piece = self.piece_factory.get_random_piece()
            # Spawn first piece
            self.spawn_next_piece()

    def pause(self) -> None:
        """
        Pause the game.

        Only allowed when in PLAYING state.
        """
        if self.state == 'PLAYING':
            self.state = 'PAUSED'

    def resume(self) -> None:
        """
        Resume a paused game.

        Only allowed when in PAUSED state.
        """
        if self.state == 'PAUSED':
            self.state = 'PLAYING'

    def end_game(self) -> None:
        """
        End the game.

        Transitions to GAME_OVER state and updates high score.
        """
        self.state = 'GAME_OVER'
        self.score_manager.update_high_score()

    def spawn_next_piece(self) -> None:
        """
        Spawn the next piece as the current piece.

        Takes the next_piece and makes it current, then generates
        a new next_piece for preview. This implements the preview
        system (REQ-8).
        """
        # Move next piece to current
        self.current_piece = self.next_piece
        # Reset position to spawn location
        if self.current_piece:
            self.current_piece.row = 0
            self.current_piece.col = 3
        # Generate new next piece
        self.next_piece = self.piece_factory.get_random_piece()

    def try_spawn_piece(self) -> bool:
        """
        Attempt to spawn a new piece.

        Checks if the spawn area is clear. If blocked, triggers
        game over (REQ-7).

        Returns:
            True if spawn successful, False if blocked (game over)
        """
        if self.current_piece is None:
            self.spawn_next_piece()

        # Check if current piece position is valid
        if not self.collision_detector.is_valid_move(
            self.current_piece,
            self.current_piece.row,
            self.current_piece.col
        ):
            # Cannot spawn - game over
            self.end_game()
            return False

        return True

    def lock_current_piece(self) -> None:
        """
        Lock the current piece to the board.

        Places all blocks of the current piece on the board,
        then checks for completed lines and clears them.
        """
        if self.current_piece is None:
            return

        # Place piece blocks on board
        positions = self.current_piece.get_block_positions()
        color = self.current_piece.color

        for row, col in positions:
            self.board.set_cell(row, col, color)

        # Check for completed lines
        complete_lines = self.board.get_complete_lines()
        if complete_lines:
            # Clear the lines
            self.board.clear_lines(complete_lines)
            # Award score
            num_lines = len(complete_lines)
            self.score_manager.add_line_clear_score(num_lines)

        # Clear current piece (will spawn new one next)
        self.current_piece = None

    def check_game_over(self) -> None:
        """
        Check if game over condition is met.

        Game over occurs when blocks are present in spawn area
        (top row). Related to REQ-7.
        """
        if self.board.is_game_over():
            self.end_game()

    def get_drop_speed(self) -> int:
        """
        Get the current drop speed in milliseconds.

        Drop speed increases (interval decreases) with level (REQ-6).
        Formula: base_speed - (level - 1) * speed_decrease
        Minimum speed enforced to maintain playability.

        Returns:
            Drop interval in milliseconds
        """
        level = self.score_manager.get_level()

        # Base drop speed at level 1
        base_speed = 1000  # 1 second per row

        # Speed increase per level
        speed_decrease = 100  # 100ms faster per level

        # Calculate speed
        drop_speed = base_speed - ((level - 1) * speed_decrease)

        # Enforce minimum speed (maximum difficulty)
        min_speed = 50  # Don't go faster than 50ms
        drop_speed = max(drop_speed, min_speed)

        return drop_speed

    def get_current_level(self) -> int:
        """
        Get the current level.

        Returns:
            Current level from score manager
        """
        return self.score_manager.get_level()

    def get_final_score(self) -> int:
        """
        Get the final score.

        Used for displaying score on game over screen.

        Returns:
            Final score value
        """
        return self.score_manager.get_score()

    def reset(self) -> None:
        """
        Reset the game for a new game.

        Clears board, resets score (but keeps high score),
        returns to START state, and clears pieces.
        """
        self.state = 'START'
        self.board.reset()
        self.score_manager.reset()
        self.current_piece = None
        self.next_piece = None
