from tbs.wrapper import Wrapper
from tic_tac_toe.data.events import TTTEventFactory
from tic_tac_toe.data.game import TicTacToeGame


class TicTacToeWrapper(Wrapper):
    cls_game = TicTacToeGame
    event_factory = TTTEventFactory
