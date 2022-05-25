import pygame
from pygame.constants import BLEND_RGB_MULT
from pygame.math import Vector2

from abc import abstractmethod

from control import colors
from control.grid_position import GridPosition
from control.settings import Settings


class Button:
    """Abstract button class for user interface buttons"""

    def __init__(self, image_path: str, position: GridPosition, color: tuple[int, ...]):
        # basic attributes
        self.image = pygame.image.load(image_path).convert_alpha()
        self.position = position

        # scale image
        image_size = Vector2(self.image.get_size())
        scaling_factor = Settings.button_icon_size / image_size.x
        self.image_size = tuple(scaling_factor * image_size)
        self.image = pygame.transform.smoothscale(self.image, self.image_size)

        # color button image
        self.image.fill(color, special_flags=BLEND_RGB_MULT)
        background = pygame.Surface(self.image_size)
        background.fill(colors.background)
        background.blit(self.image, (0, 0))
        self.image = background

        # set rect
        self.rect = self.image.get_rect()
        self.rect.center = position.get_coords_center()

    def is_clicked(self, mouse_pos: tuple) -> bool:
        """Check if button is clicked"""
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    @abstractmethod
    def click(self, *args, **kwargs):
        """Abstract method for action that button makes"""
        return
