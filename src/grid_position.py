from settings import Settings
from pygame.math import Vector2


class GridPosition:
    """Class to manage coordinates of game objects on game board"""

    def __init__(self, grid_square_pos: Vector2 | tuple):
        self.grid_square_pos = Vector2(grid_square_pos)

    def get_coords(self) -> Vector2:
        """Get exact pixel position on upper right corner of the object"""
        return (self.grid_square_pos + Settings.window_margin) * Settings.grid_size

    def get_coords_center(self) -> Vector2:
        """Get center of specified grid square in pixels"""
        return self.get_coords() + Vector2(Settings.grid_size, Settings.grid_size) / 2
