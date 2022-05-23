import pygame

from settings import Settings


class Screen:
    """Class to store screen rect and surface"""

    surface = pygame.display.set_mode(Settings.resolution)
    rect = surface.get_rect()
