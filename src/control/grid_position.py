from control.settings import Settings
from pygame.math import Vector2


class GridPosition:
    """Class to manage coordinates of game objects on game board"""

    def __init__(self, grid_square_pos: Vector2 | tuple):
        """
        :return: None
        :param grid_square_pos: Column and row of grid square relative to board
        """
        self.grid_square_pos = Vector2(grid_square_pos)

    def get_coords(self) -> Vector2:
        """
        Get exact pixel position on upper right corner of the object

        :return: Vector of pixel coordinates of topleft corner of grid square
        """
        return (self.grid_square_pos + Settings.window_margin) * Settings.grid_size

    def get_coords_center(self) -> Vector2:
        """
        Get center of specified grid square in pixels

        :return: Vector of pixel coordinates of the center of grid square
        """
        return self.get_coords() + Vector2(Settings.grid_size, Settings.grid_size) / 2
