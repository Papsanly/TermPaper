import pygame

from assets.arrow import Arrow
from control import colors
from control.grid_position import GridPosition
from control.settings import Settings
from assets.grid_square import GridSquare
from assets.number import Number
from utils.core_logic import CoreLogic


class Board:
    """Class for game board that holds arrows and numbers"""

    def __init__(self):
        # frame that surrounds grid squares that hold numbers
        self.frame_size = tuple(Settings.grid_count * Settings.grid_size)
        self.frame_rect = pygame.Rect(
            tuple(GridPosition((0, 0)).get_coords()),
            self.frame_size
        )
        self.frame_color = colors.board_frame
        self.frame_width = 5

        # generate random values matrix for number grid squares
        self.values = CoreLogic.gen_values()

        # create grid squares group that hold numbers
        self.numbers = pygame.sprite.Group()
        for row, values_row in enumerate(self.values):
            for col, value in enumerate(values_row):
                self.numbers.add(GridSquare(
                    Number(value).image,
                    GridPosition((col, row)),
                    False
                ))

        # create empty grid squares that hold arrows
        self.arrows = pygame.sprite.Group()
        for arrows_set_direction, arrows_set in CoreLogic.arrows.items():
            for arrow_num, arrow in enumerate(arrows_set):
                self.arrows.add(GridSquare(
                    Arrow(arrow).image,
                    GridPosition(CoreLogic.get_position(arrows_set_direction, arrow_num)),
                    True
                ))

    def draw(self, surface: pygame.Surface):
        """Draw object to given surface"""
        # draw numbers grid squares
        self.numbers.draw(surface)

        # draw arrows grid squares
        self.arrows.draw(surface)

        # draw frame
        pygame.draw.rect(surface, self.frame_color, self.frame_rect, self.frame_width)
