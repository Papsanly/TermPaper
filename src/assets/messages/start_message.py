from assets.messages.message import Message
from utils.collide_rect_evaluetor import CollideRectEvaluator


class StartMessage(Message):
    """Message that appears before the game starts"""

    def __init__(self):
        super().__init__('../assets/messages/message_start.png')
        collide_rect_ratios = [(557 / 2000, 544 / 1000), (1459 / 2000, 837 / 1000)]
        self.collide_rect = CollideRectEvaluator.evaluate_from_ratios(collide_rect_ratios, self.rect)
