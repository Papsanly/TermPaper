import pygame

from grid_square import GridSquare


class NumberGridSquare(GridSquare):
    """Grid square that holds a number"""

    def __init__(self):
        super().__init__()
        