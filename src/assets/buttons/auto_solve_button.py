from assets.buttons.button import Button
from control import colors
from control.grid_position import GridPosition
from control.settings import Settings


class AutoSolveButton(Button):
    """Button automaticaly solving the puzzle"""

    def __init__(self):
        super().__init__(
            '../assets/buttons/auto_solve_button.png',
            GridPosition((Settings.grid_count.x + 1, -2)),
            colors.arrows_button,
            False,
            Settings.button_icon_size / 400
        )

    def handle_click(self):
        pass
