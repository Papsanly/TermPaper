import pygame


class CollideRectEvaluator:

    @classmethod
    def evaluate_from_ratios(cls, ratios, base_rect: pygame.Rect) -> pygame.Rect:
        collide_rect_width = (ratios[1][0] - ratios[0][0]) * base_rect.width
        collide_rect_top = base_rect.top + ratios[0][1] * base_rect.height
        collide_rect_left = base_rect.left + ratios[0][0] * base_rect.width
        collide_rect_height = (ratios[1][1] - ratios[0][1]) * base_rect.height

        collide_rect = pygame.Rect(
            (collide_rect_left, collide_rect_top),
            (collide_rect_width, collide_rect_height)
        )

        return collide_rect
