import pygame
from pygame.math import Vector2

from control.screen import Screen
from control.settings import Settings


class Message:
    """Base class for messages"""

    def __init__(self, image_path: str):
        """
        :return: None
        :param image_path: Path to message image path
        """
        # get and scale image
        self.image = pygame.image.load(image_path).convert_alpha()
        size = self.image.get_size()
        scaling_factor = Settings.message_size / size[0]
        new_size = tuple(scaling_factor * Vector2(size))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.image_size = self.image.get_size()

        # get and center rect
        self.rect = self.image.get_rect()
        self.rect.center = Settings.get_resolution() // 2

    def draw(self) -> None:
        Screen.surface.blit(self.image, self.rect)
