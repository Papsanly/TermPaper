import pygame

from control import colors
from control.settings import Settings


class Number:
    """Class for number image to render on game board"""

    def __init__(self, value: int):
        # get text font and related attributes
        self.color = colors.numbers
        self.font = pygame.font.SysFont('BAUHS93', Settings.number_size)

        # render image
        self.image = self.font.render(str(value), True, self.color, colors.background)
