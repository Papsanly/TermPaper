from pygame import Vector2

from assets.buttons.button import Button
from control import colors
from control.grid_position import GridPosition
from control.settings import Settings


class EndSessionButton(Button):
    """Button class for ending session and checking if player won"""

    def __init__(self):
        super().__init__(
            '../assets/buttons/end_session_button.png',
            GridPosition(Settings.grid_count + Vector2(0, 2)),
            colors.end_session_button
        )

    def handle_click(self):
        """Handles in main game class"""
        return
