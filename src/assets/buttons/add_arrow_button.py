from assets.arrow import Arrow
from assets.buttons.button import Button
from control import colors
from control.grid_position import GridPosition
from control.settings import Settings


class AddArrowButton(Button):
    """Buttons for adding and replacing"""

    def __init__(self, direction: tuple, position: int):
        super().__init__(
            f'../assets/buttons/arrow{direction}.png',
            GridPosition((position - 2, Settings.grid_count.y + 2)),
            colors.arrows_button,
            False,
            Settings.button_icon_size / 500
        )
        self.direction = direction

    def handle_click(self) -> tuple[Arrow, tuple[int, int], tuple[int]]:
        """Return new arrow image of given direction to set as image attribute of selected square"""
        return Arrow(self.direction).image, self.direction, colors.highlighted_blue
