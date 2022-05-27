from assets.messages.message import Message
from utils.collide_rect_evaluetor import CollideRectEvaluator


class WrongMessage(Message):
    """Message that appears before the game starts"""

    def __init__(self):
        super().__init__('../assets/messages/message_wrong.png')
        collide_rect_ratios_continue = [(131 / 2000, 604 / 1000), (826 / 2000, 832 / 1000)]
        collide_rect_ratios_quit = [(1149 / 2000, 604 / 1000), (1843 / 2000, 832 / 1000)]
        self.collide_rect_continue = CollideRectEvaluator.evaluate_from_ratios(collide_rect_ratios_continue, self.rect)
        self.collide_rect_quit = CollideRectEvaluator.evaluate_from_ratios(collide_rect_ratios_quit, self.rect)
