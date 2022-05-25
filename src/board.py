import pygame

import colors
from grid_position import GridPosition
from grid_square import GridSquare
from number import Number
from screen import Screen
from settings import Settings
from utils import Utils


class Board:
    """Class for game board that holds arrows and numbers"""

    def __init__(self):
        # frame that surrounds grid squares that hold numbers
        self.frame_size = (8 * Settings.grid_size, 8 * Settings.grid_size)
        self.frame_rect = pygame.Rect(
            tuple(GridPosition((0, 0)).get_coords()),
            self.frame_size
        )
        self.frame_color = colors.board_frame
        self.frame_width = 5

        # generate random numbers matrix for number grid squares
        self.values = Utils.gen_values()

        # create grid squares group that hold numbers
        self.numbers = pygame.sprite.Group()
        for row, values_row in enumerate(self.values):
            for col, value in enumerate(values_row):
                self.numbers.add(GridSquare(
                    Number(value).image,
                    GridPosition((col, row)),
                    False
                ))

    def draw(self, surface: pygame.Surface):
        """Draw object to given surface"""
        # draw numbers
        self.numbers.draw(surface)

        # draw frame
        pygame.draw.rect(surface, self.frame_color, self.frame_rect, self.frame_width)
