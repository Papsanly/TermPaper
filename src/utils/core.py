import random

import pygame.sprite
from pygame.math import Vector2

from control.settings import Settings


class Core:
    """Class for various functions and variables for core game logic"""

    arrow_directions: list[tuple[int, int]] = [
        (1, -1), (1, 0), (1, 1), (0, 1),
        (-1, 1), (-1, 0), (-1, -1), (0, -1),
    ]

    arrow_sets: dict[tuple[int, int], list[tuple[int, int]]] = {
        (0, -1): ((0, 1), (1, 1), (-1, 1)),
        (1, 0): ((-1, 0), (-1, 1), (-1, -1)),
        (-1, 0): ((1, 0), (1, 1), (1, -1)),
        (0, 1): ((0, -1), (1, -1), (-1, -1))
    }

    forbidden_directions: dict[tuple[int, int], list[tuple[int, int]]] = {
        (0, -1): [(-1, 1), (1, 1)],
        (1, 0): [(-1, -1), (-1, 1)],
        (-1, 0): [(1, -1), (1, 1)],
        (0, 1): [(-1, -1), (1, -1)]
    }

    arrows: dict[tuple[int, int], list[tuple[int, int]]] = {}
    numbers: list[list[int]] = []

    @classmethod
    def gen_arrows(cls) -> None:
        """
        Generate arrows dict with keys as direction on game board and list of arrows as values
        """

        arrows = {}
        for arrow_set in cls.arrow_sets:
            arrows[arrow_set] = []
            grid_count = Settings.grid_count.x if arrow_set in [(0, -1), (0, 1)] else Settings.grid_count.y
            for i in range(int(grid_count)):
                possible_directions = cls.get_possible_directions(arrow_set, i)
                choice = random.choice(possible_directions)
                arrows[arrow_set].append(choice)

        cls.arrows = arrows

    @classmethod
    def get_possible_directions(cls, arrow_set: tuple[int, int], arrow_num: int) -> list[tuple[int, int]]:
        """
        Get possible arrow directions for given arrow location

        :return: List of possible directions that arrow can point to
        :param arrow_set: Direction in which the arrow is located
        :param arrow_num: Sequence number of arrow on arrow set counting from up or left
        """
        grid_count = Settings.grid_count.x if arrow_set in [(0, -1), (0, 1)] else Settings.grid_count.y
        possible_directions = list(cls.arrow_sets[arrow_set])
        if arrow_num == 0:
            possible_directions.remove(cls.forbidden_directions[arrow_set][0])
        if arrow_num == grid_count - 1:
            possible_directions.remove(cls.forbidden_directions[arrow_set][1])
        return possible_directions

    @classmethod
    def get_position(cls, arrows_set_direction: tuple[int, int], arrow_num: int) -> Vector2:
        """
        Get position relative to board of given arrow

        :return: Position vector of arrow relative to game board
        :param arrows_set_direction: Direction in which the arrow is located
        :param arrow_num: Sequence number of arrow on arrow set counting from up or left
        """
        if arrows_set_direction == (0, -1):
            position = arrow_num, -1
        elif arrows_set_direction == (1, 0):
            position = Settings.grid_count.x, arrow_num
        elif arrows_set_direction == (-1, 0):
            position = -1, arrow_num
        elif arrows_set_direction == (0, 1):
            position = arrow_num, Settings.grid_count.y
        else:
            raise ValueError('arrow set direction not valid')

        return Vector2(position)

    @classmethod
    def get_span(cls, position: Vector2, arrow: tuple[int, int] | None = None) -> list[Vector2, ...]:
        """
        Get all grid squares that given arrow points to

        :return: List of grid square positions that given arrow points to
        :param position: Position vector of arrow relative to game board
        :param arrow: Direction in which arrow points to
        """
        if not arrow:
            return []

        grid_squares = []
        grid_square = position.copy()
        while True:
            grid_square += Vector2(arrow)

            rect = pygame.Rect((0, 0), tuple(Settings.grid_count))
            if not rect.collidepoint(tuple(grid_square)):
                break

            grid_squares.append(grid_square.copy())

        return grid_squares

    @classmethod
    def get_pointings(cls, grid_square: Vector2) -> list[tuple[tuple[int, int], int]]:
        """
        Get arrows that point to specified location on board

        :return: List of arrow sets and arrow numbers that point to given grid square
        :param grid_square: Position of grid square relative to board
        """
        result = []
        for arrows_set_direction, arrows_set in cls.arrows.items():
            for arrow_num, arrow in enumerate(arrows_set):
                position = cls.get_position(arrows_set_direction, arrow_num)
                if arrow:
                    if grid_square in cls.get_span(position, arrow):
                        result.append((arrows_set_direction, arrow_num))
        return result

    @classmethod
    def count_pointings(cls, grid_square: Vector2) -> int:
        """
        Count number of arrows that point to specified location on board

        :return: Number of arrows that point to given grid square
        :param grid_square: Position of grid square relative to board
        """
        return len(cls.get_pointings(grid_square))

    @classmethod
    def evaluate_correctness(cls) -> list[tuple[int, int]]:
        """
        Get all numbers that don't match with number of arrows that point to them

        :return: List of numbers, values of which don't match with number of arrows that point to them
        """
        wrong_numbers = []
        for col, numbers_col in enumerate(cls.numbers):
            for row, number in enumerate(numbers_col):
                if number != cls.count_pointings(Vector2(col, row)):
                    wrong_numbers.append((col, row))
        return wrong_numbers

    @classmethod
    def gen_numbers(cls) -> None:
        """
        Generate numbers matrix based on previously generated arrows
        """
        cls.gen_arrows()

        cls.numbers = [
            [
                cls.count_pointings(Vector2(col, row))
                for row in range(int(Settings.grid_count.y))
            ]
            for col in range(int(Settings.grid_count.x))
        ]
