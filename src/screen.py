import pygame
from dataclasses import dataclass

from settings import Settings


@dataclass
class Screen:
    """Class to store screen rect and surface"""

    surface = pygame.display.set_mode(Settings.get_resolution())
    rect = surface.get_rect()
    bg_color = (29, 29, 38)

    @classmethod
    def set_caption(cls, name: str) -> None:
        """Set caption for game window"""
        pygame.display.set_caption(name)
