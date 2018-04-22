from chess.wrapper import ChessWrapper
from core.managers import UpdateManager, ReplayManager
from settings import SAVE_DIR


class ChessUpdateManager(UpdateManager):
    cls_wrapper = ChessWrapper
    base_save_dir = SAVE_DIR['chess']


class ChessReplayManager(ReplayManager):
    cls_wrapper = ChessWrapper
    base_save_dir = SAVE_DIR['chess']
