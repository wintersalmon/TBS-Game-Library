from chess.events import ChessEventFactory
from chess.game import ChessGame
from tbs.wrapper import Wrapper


class ChessWrapper(Wrapper):
    cls_game = ChessGame
    cls_event_factory = ChessEventFactory
