from dataclasses import dataclass


@dataclass
class States:
    """Class to store all and current game states"""

    # all game states
    GAME_ACTIVE: int = 0
    GAME_START: int = 1
    GAME_END_CORRECT: int = 2
    GAME_END_WRONG: int = 3

    # current game state
    current_state = GAME_START
    