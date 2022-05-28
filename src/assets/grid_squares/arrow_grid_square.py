import pygame

from assets.grid_squares.grid_square import GridSquare
from control.grid_position import GridPosition
from utils.core import Core


class ArrowGridSquare(GridSquare):
    """Subclass of grid square to hold arrows and related attributes"""

    def __init__(self, content: pygame.Surface | None,
                 arrow_set: tuple[int, int], arrow_num: int,
                 direction: tuple[int, int] | None = None):
        """
        :return: None
        :param arrow_set: Direction in which the arrow is located
        :param arrow_num: Sequence number of arrow on arrow set counting from up or left
        """
        super().__init__(content)
        self.arrow_set = arrow_set
        self.arrow_num = arrow_num
        self.position = GridPosition(Core.get_position(arrow_set, arrow_num))
        self.rect.topleft = self.position.get_coords()
        self.direction = direction

    def set_image(self, image: pygame.Surface, direction: tuple[int, int]) -> None:
        """
        Set arrow image for arrow grid square

        :return: None
        :param image: Arrow image to fill the arrow grid square
        :param direction: Direction that arrow points to
        """
        self.__init__(image, self.arrow_set, self.arrow_num, direction)
