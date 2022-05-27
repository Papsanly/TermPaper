from assets.buttons.button import Button
from control import colors
from control.grid_position import GridPosition
from control.settings import Settings


class DeleteArrowButton(Button):
    """Buttons for deleting arrows"""

    def __init__(self, position: int):
        super().__init__(
            '../assets/buttons/delete_arrow_button.png',
            GridPosition((position - 2, Settings.grid_count.y + 2)),
            colors.delete_arrow_button
        )

    def handle_click(self):
        """Handles in main game class"""
        return
