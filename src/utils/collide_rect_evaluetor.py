import pygame


class CollideRectEvaluator:
    """Evaluates collision rects for message buttons"""

    @classmethod
    def evaluate_from_ratios(cls, ratios: list[tuple[float, float]], base_rect: pygame.Rect) -> pygame.Rect:
        """
        Get collision rect for message buttons

        :return: Collision rect for message buttons
        :param ratios: Coordinates of collide rect box divided by image size
        :param base_rect: Rect of image that holds collide rect
        """
        collide_rect_width = (ratios[1][0] - ratios[0][0]) * base_rect.width
        collide_rect_top = base_rect.top + ratios[0][1] * base_rect.height
        collide_rect_left = base_rect.left + ratios[0][0] * base_rect.width
        collide_rect_height = (ratios[1][1] - ratios[0][1]) * base_rect.height

        collide_rect = pygame.Rect(
            (collide_rect_left, collide_rect_top),
            (collide_rect_width, collide_rect_height)
        )

        return collide_rect
