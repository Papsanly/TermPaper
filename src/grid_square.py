import pygame

from pygame.math import Vector2

import colors
from grid_position import GridPosition
from settings import Settings


class GridSquare(pygame.sprite.Sprite):
    """Class for grid square objects that hold arrows or numbers"""

    def __init__(self, content: pygame.Surface, position: GridPosition, is_selectable: bool):
        super().__init__()
        # position relative to board with arrows
        self.position = position

        # frame that surrounds the square
        self.frame_size = (Settings.grid_size, Settings.grid_size)
        self.frame_rect = pygame.Rect((0, 0), self.frame_size)
        self.frame_width = 1
        self.frame_color = colors.grid_square_frames

        # get content rect
        self.content_image = content
        self.content_rect = content.get_rect()
        self.content_rect.center = Vector2(Settings.grid_size, Settings.grid_size) / 2

        # indicator if grid square is selectable
        self.is_selectable = is_selectable

        # get image and rect for sprite.draw() method
        self.image = pygame.Surface(self.frame_size)
        self.image.fill(colors.background)
        pygame.draw.rect(self.image, self.frame_color, self.frame_rect, self.frame_width)
        self.image.blit(self.content_image, self.content_rect)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position.get_coords()
