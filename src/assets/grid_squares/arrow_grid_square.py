import pygame

from assets.grid_squares.grid_square import GridSquare
from control.grid_position import GridPosition
from utils.core import Core


class ArrowGridSquare(GridSquare):
    """Subclass of grid square to hold arrows and related attributes"""

    def __init__(self, content: pygame.Surface | None,
                 arrow_set: tuple[int, int], arrow_num: int, direction: tuple[int, int] | None = None):
        super().__init__(content)
        self.arrow_set = arrow_set
        self.arrow_num = arrow_num
        self.position = GridPosition(Core.get_position(arrow_set, arrow_num))
        self.rect.topleft = self.position.get_coords()
        self.direction = direction

    def set_image(self, image: pygame.Surface, direction):
        """Set arrow image for arrow grid square"""
        self.__init__(image, self.arrow_set, self.arrow_num, direction)
