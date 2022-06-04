from dataclasses import dataclass

from pygame.math import Vector2


@dataclass(frozen=True)
class Settings:
    """Class to store settings for the app"""

    # basic settings
    grid_count: Vector2 = Vector2(8, 8)
    window_margin: Vector2 = Vector2(2, 2)
    grid_size: int = 60
    fps: int = 30

    # arrows settings
    arrow_size: int = 35

    # numbers size
    number_size: int = 48

    # button settings
    button_icon_size: int = 40

    # message settings
    message_size: int = 500

    @classmethod
    def get_resolution(cls) -> Vector2:
        """
        Get actual pixel resolution of entire screen

        :return: Actual pixel resolution of entire screen
        """
        return (cls.grid_count + 2 * cls.window_margin + Vector2(0, 1)) * cls.grid_size
