import pygame
from dataclasses import dataclass

from control import colors
from control.settings import Settings


@dataclass
class Screen:
    """Class to store screen rect and surface"""

    surface = pygame.display.set_mode(Settings.get_resolution())
    rect = surface.get_rect()
    bg_color = colors.background

    @classmethod
    def set_caption(cls, name: str) -> None:
        """
        Set caption for game window

        :return: None
        :param name: Name for window caption
        """
        pygame.display.set_caption(name)
