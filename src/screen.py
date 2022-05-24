import pygame

from settings import Settings


class Screen:
    """Class to store screen rect and surface"""

    surface = pygame.display.set_mode(Settings.get_resolution())
    rect = surface.get_rect()

    @classmethod
    def set_caption(cls, name):
        """Set caption for game window"""
        pygame.display.set_caption(name)
