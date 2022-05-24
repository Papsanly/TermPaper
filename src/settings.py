from dataclasses import dataclass

from pygame.math import Vector2


@dataclass(frozen=True)
class Settings:
    """Class to store settings for the app"""

    grid_count: Vector2 = Vector2(12, 12)
    grid_size: int = 75
    fps = 120

    @classmethod
    def get_resolution(cls) -> Vector2:
        """Get actual pixel resolution of entire screen"""
        return cls.grid_count * cls.grid_size
