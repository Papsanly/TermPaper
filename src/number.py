import pygame

import colors


class Number:
    """Class for number image to render on game board"""

    def __init__(self, value: int):
        # get text font and related attributes
        self.color = colors.numbers
        self.font = pygame.font.SysFont('BAUHS93', 48)

        # render image
        self.image = self.font.render(str(value), True, self.color, colors.background)
