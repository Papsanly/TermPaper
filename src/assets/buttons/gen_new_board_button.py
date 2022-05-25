from pygame.math import Vector2

from assets.board import Board
from assets.buttons.button import Button
from control import colors
from control.grid_position import GridPosition
from control.settings import Settings


class GenNewBoardButton(Button):
    """Button class for genereting new board"""

    def __init__(self):
        super().__init__(
            '../assets/buttons/gen_new_board_button.png',
            GridPosition(Settings.grid_count + Vector2(1, 1)),
            colors.new_board_button
        )

    def click(self) -> Board:
        """Generate new values of board numbers when button is clicked"""
        return Board()
