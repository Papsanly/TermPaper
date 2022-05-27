import pygame
from pygame.constants import BLEND_RGB_ADD, BLEND_RGB_SUB

from assets.grid_squares.grid_square import GridSquare
from control import colors
from control.grid_position import GridPosition


class NumberGridSquare(GridSquare):
    """Subclass of grid square to hold arrows and related attributes"""

    def __init__(self, content: pygame.Surface | None,
                 col: int, row: int, value: int):
        super().__init__(content)
        self.col = col
        self.row = row
        self.value = value
        self.position = GridPosition((col, row))
        self.rect.topleft = self.position.get_coords()

    def highlight_error(self):
        self.image.fill(colors.highlight_red, special_flags=BLEND_RGB_ADD)

    def dehighlight_error(self):
        self.image.fill(colors.highlight_red, special_flags=BLEND_RGB_SUB)
