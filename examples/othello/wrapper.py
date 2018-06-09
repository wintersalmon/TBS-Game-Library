from othello.events import OthelloEventFactory
from othello.game import OthelloGame
from tbs.wrapper import Wrapper


class OthelloWrapper(Wrapper):
    cls_game = OthelloGame
    cls_event_factory = OthelloEventFactory
