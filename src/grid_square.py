import pygame

from grid_position import GridPosition
from settings import Settings


class GridSquare:
    """Abstract class for grid square objects that hold arrows or numbers"""

    def __init__(self, position: tuple):
        # position on screen surface
        self.position = GridPosition(position)

        # frame that surrounds the square
        self.frame_size = (Settings.grid_size, Settings.grid_size)
        self.frame_rect = pygame.Rect(self.position.get_coords(), self.frame_size)
        self.frame_width = 5
        self.frame_color = (191, 194, 198)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.frame_color, self.frame_rect, self.frame_width)
