from core.managers import ReplayManager, UpdateManager
from settings import SAVE_DIR
from .wrapper import TicTacToeWrapper


class TicTacToeReplayManager(ReplayManager):
    cls_wrapper = TicTacToeWrapper
    base_save_dir = SAVE_DIR['tic_tac_toe']


class TicTacToeUpdateManager(UpdateManager):
    cls_wrapper = TicTacToeWrapper
    base_save_dir = SAVE_DIR['tic_tac_toe']
