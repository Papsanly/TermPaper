import pygame

from grid_position import GridPosition
from settings import Settings


class Board:
    """Class for game board that holds arrows and numbers"""

    def __init__(self):
        # frame that surrounds grid squares that hold numbers
        self.frame_size = (8 * Settings.grid_size, 8 * Settings.grid_size)
        self.frame_rect = pygame.Rect(
            tuple(GridPosition((2, 2)).get_coords()),
            self.frame_size
        )
        self.frame_color = (211, 185, 49)
        self.frame_width = 5

        # generate random numbers matrix for number grid squares
        self.values = [
            [
                randint()
            ]
        ]

        # create grid squares that hold numbers


    def draw(self, surface: pygame.Surface):
        """Draw object to given surface"""
        # draw frame
        pygame.draw.rect(surface, self.frame_color, self.frame_rect, self.frame_width)
