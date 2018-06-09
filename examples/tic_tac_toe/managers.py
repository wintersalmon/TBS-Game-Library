from tic_tac_toe.config import APP_SAVE_DIR
from tbs.managers import ReplayManager, UpdateManager
from tic_tac_toe.wrapper import TicTacToeWrapper


class TicTacToeReplayManager(ReplayManager):
    cls_wrapper = TicTacToeWrapper
    base_save_dir = APP_SAVE_DIR


class TicTacToeUpdateManager(UpdateManager):
    cls_wrapper = TicTacToeWrapper
    base_save_dir = APP_SAVE_DIR
