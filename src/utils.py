import random

from pygame.math import Vector2

from settings import Settings


class Utils:
    """Class for various functions for core game logic"""

    @classmethod
    def gen_arrows(cls) -> dict[tuple[int, int], list[tuple[int, int], ...]]:
        """Generate arrows dict with keys as direction on game board and list of arrows as values"""
        arrow_sets = {
            (0, -1): ((0, 1), (1, 1), (-1, 1)),
            (1, 0): ((-1, 0), (-1, 1), (-1, -1)),
            (-1, 0): ((1, 0), (1, 1), (1, -1)),
            (0, 1): ((0, -1), (1, -1), (-1, -1))
        }

        forbidden_directions = {
            (0, -1): {0: (-1, 1), 7: (1, 1)},
            (1, 0): {0: (-1, -1), 7: (-1, 1)},
            (-1, 0): {0: (1, -1), 7: (1, 1)},
            (0, 1): {0: (-1, -1), 7: (1, -1)}
        }

        arrows = {}
        for arrow_set, arrow_directions in arrow_sets.items():
            arrows[arrow_set] = []
            grid_count = Settings.grid_count.x if arrow_set in [(0, -1), (0, 1)] else Settings.grid_count.y
            for i in range(int(grid_count)):
                possible_directions = list(arrow_directions)
                if i in [0, 7]:
                    possible_directions.remove(forbidden_directions[arrow_set][i])
                choice = random.choice(possible_directions)
                arrows[arrow_set].append(choice)

        return arrows

    @classmethod
    def get_position(cls, arrows_set: tuple[int, int], arrow_num: int) -> Vector2:
        """Get position relative to board of given arrow"""
        position = Vector2()
        if arrows_set == (0, -1):
            position = arrow_num, -1
        elif arrows_set == (1, 0):
            position = Settings.grid_count.x, arrow_num
        elif arrows_set == (-1, 0):
            position = -1, arrow_num
        elif arrows_set == (0, 1):
            position = arrow_num, Settings.grid_count.y

        return position

    @classmethod
    def get_span(cls, position: Vector2, arrow: tuple[int, int]) -> list[Vector2, ...]:
        """Get all grid squares that given arrow points to"""
        grid_squares = []

        grid_square = Vector2(0, 0)
        i = 1
        while grid_square.x < 7 and grid_square.y < 7:
            grid_square = position + i * Vector2(arrow)
            grid_squares.append(grid_square)
            i += 1

        return grid_squares

    @classmethod
    def count_pointings(cls, grid_square: Vector2,
                        arrows: dict[tuple[int, int], list[tuple[int, int], ...]]) -> int:
        """Count number of arrows that point to specified location on board"""
        result = 0
        for arrows_set_direction, arrows_set in arrows.items():
            for arrow_num, arrow in enumerate(arrows_set):
                position = cls.get_position(arrows_set_direction, arrow_num)
                if grid_square in cls.get_span(position, arrow):
                    result += 1
        return result

    @classmethod
    def gen_values(cls) -> list[list[int, ...], ...]:
        """Generate values matrix based on previously generated arrows"""
        arrows = cls.gen_arrows()
        values = [
            [
                cls.count_pointings(Vector2(col, row), arrows)
                for col in range(int(Settings.grid_count.y))
            ]
            for row in range(int(Settings.grid_count.x))
        ]
        return values
