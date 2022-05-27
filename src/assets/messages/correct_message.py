from assets.messages.message import Message
from utils.collide_rect_evaluetor import CollideRectEvaluator


class CorrectMessage(Message):
    """Message that appears before the game starts"""

    def __init__(self):
        super().__init__('../assets/messages/message_correct.png')
        collide_rect_ratios_again = [(144 / 2000, 660 / 1000), (838 / 2000, 887 / 1000)]
        collide_rect_ratios_quit = [(1162 / 2000, 660 / 1000), (1856 / 2000, 887 / 1000)]
        self.collide_rect_again = CollideRectEvaluator.evaluate_from_ratios(collide_rect_ratios_again, self.rect)
        self.collide_rect_quit = CollideRectEvaluator.evaluate_from_ratios(collide_rect_ratios_quit, self.rect)
