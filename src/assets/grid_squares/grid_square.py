import pygame
from pygame.constants import BLEND_RGB_ADD, BLEND_RGB_SUB
from pygame.math import Vector2

from control import colors
from control.screen import Screen
from control.settings import Settings


class GridSquare:
    """Class for grid square objects that hold arrows or numbers"""

    def __init__(self, content: pygame.Surface | None):
        super().__init__()
        # frame that surrounds the square
        self.frame_size = (Settings.grid_size, Settings.grid_size)
        self.frame_rect = pygame.Rect((0, 0), self.frame_size)
        self.frame_width = 1
        self.frame_color = colors.grid_square_frames

        # get content rect
        if content:
            self.content_image = content
            self.content_rect = content.get_rect()
            self.content_rect.center = Vector2(Settings.grid_size, Settings.grid_size) / 2

        # Indicator for toggling selection and related attributes
        self.selected = False

        # get image and rect for sprite.draw() method
        self.image = pygame.Surface(self.frame_size)
        self.image.fill(colors.background)
        pygame.draw.rect(self.image, self.frame_color, self.frame_rect, self.frame_width)
        if content:
            self.image.blit(self.content_image, self.content_rect)

        self.rect = self.image.get_rect()

    def draw(self):
        Screen.surface.blit(self.image, self.rect)

    def select(self, highlight_color):
        self.selected = True
        self.image.fill(highlight_color, special_flags=BLEND_RGB_ADD)

    def deselect(self, highlight_color):
        self.selected = False
        self.image.fill(highlight_color, special_flags=BLEND_RGB_SUB)
