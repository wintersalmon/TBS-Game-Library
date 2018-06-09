from chess.wrapper import ChessWrapper
from chess.config import APP_SAVE_DIR
from tbs.managers import UpdateManager, ReplayManager


class ChessUpdateManager(UpdateManager):
    cls_wrapper = ChessWrapper
    base_save_dir = APP_SAVE_DIR


class ChessReplayManager(ReplayManager):
    cls_wrapper = ChessWrapper
    base_save_dir = APP_SAVE_DIR
