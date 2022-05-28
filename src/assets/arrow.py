import pygame
from pygame.constants import BLEND_RGB_MULT
from pygame.math import Vector2

from control import colors
from control.settings import Settings


class Arrow:
    """Class for rendering arrows"""

    def __init__(self, direction: tuple[int, int]):
        """
        :return: None
        :param direction: Direction of arrow to render appropriate image
        """
        # load image and scale
        arrow_image = pygame.image.load(f'../assets/arrows/{direction}.png').convert_alpha()

        image_size_vec = Vector2(arrow_image.get_size())
        scaling_factor = Settings.arrow_size / image_size_vec.length()
        self.arrow_image_size = tuple(scaling_factor * image_size_vec)

        arrow_image = pygame.transform.smoothscale(arrow_image, self.arrow_image_size)

        # fill arrow with specific color
        arrow_image.fill(colors.arrows, special_flags=BLEND_RGB_MULT)

        # background surface to draw arrow on
        background = pygame.Surface(self.arrow_image_size)
        background.fill(colors.background)

        # blit arrow to background
        background.blit(arrow_image, (0, 0))

        self.image = background
