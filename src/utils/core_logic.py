import random

import pygame.sprite
from pygame.math import Vector2

from control.settings import Settings


class CoreLogic:
    """Class for various functions and variables for core game logic"""

    arrow_sets: dict[tuple[int, int], list[tuple[int, int], ...]] = {
        (0, -1): ((0, 1), (1, 1), (-1, 1)),
        (1, 0): ((-1, 0), (-1, 1), (-1, -1)),
        (-1, 0): ((1, 0), (1, 1), (1, -1)),
        (0, 1): ((0, -1), (1, -1), (-1, -1))
    }

    forbidden_directions: dict[tuple[int, int], list[tuple[int, int], ...]] = {
        (0, -1): [(-1, 1), (1, 1)],
        (1, 0): [(-1, -1), (-1, 1)],
        (-1, 0): [(1, -1), (1, 1)],
        (0, 1): [(-1, -1), (1, -1)]
    }

    arrows: dict[tuple[int, int], list[tuple[int, int], ...]] = {}

    @classmethod
    def gen_arrows(cls):
        """Generate arrows dict with keys as direction on game board and list of arrows as values"""

        arrows = {}
        for arrow_set, arrow_directions in cls.arrow_sets.items():
            arrows[arrow_set] = []
            grid_count = Settings.grid_count.x if arrow_set in [(0, -1), (0, 1)] else Settings.grid_count.y
            for i in range(int(grid_count)):
                possible_directions = list(arrow_directions)
                if i == 0:
                    possible_directions.remove(cls.forbidden_directions[arrow_set][0])
                if i == grid_count - 1:
                    possible_directions.remove(cls.forbidden_directions[arrow_set][1])
                choice = random.choice(possible_directions)
                arrows[arrow_set].append(choice)

        cls.arrows = arrows

    @classmethod
    def get_position(cls, arrows_set_direction: tuple[int, int], arrow_num: int) -> Vector2:
        """Get position relative to board of given arrow"""
        position = Vector2()
        if arrows_set_direction == (0, -1):
            position = arrow_num, -1
        elif arrows_set_direction == (1, 0):
            position = Settings.grid_count.x, arrow_num
        elif arrows_set_direction == (-1, 0):
            position = -1, arrow_num
        elif arrows_set_direction == (0, 1):
            position = arrow_num, Settings.grid_count.y

        return position

    @classmethod
    def get_span(cls, position: Vector2, arrow: tuple[int, int]) -> list[Vector2, ...]:
        """Get all grid squares that given arrow points to"""
        grid_squares = []

        grid_square = position
        while True:
            grid_square += Vector2(arrow)

            rect = pygame.Rect((0, 0), tuple(Settings.grid_count))
            if not rect.collidepoint(tuple(grid_square)):
                break

            grid_squares.append(grid_square.copy())

        return grid_squares

    @classmethod
    def count_pointings(cls, grid_square: Vector2) -> int:
        """Count number of arrows that point to specified location on board"""
        result = 0
        for arrows_set_direction, arrows_set in cls.arrows.items():
            for arrow_num, arrow in enumerate(arrows_set):
                position = cls.get_position(arrows_set_direction, arrow_num)
                if grid_square in cls.get_span(position, arrow):
                    result += 1
        return result

    @classmethod
    def gen_values(cls) -> list[list[int, ...], ...]:
        """Generate values matrix based on previously generated arrows"""
        cls.gen_arrows()

        values = [
            [
                cls.count_pointings(Vector2(col, row))
                for col in range(int(Settings.grid_count.x))
            ]
            for row in range(int(Settings.grid_count.y))
        ]
        return values
