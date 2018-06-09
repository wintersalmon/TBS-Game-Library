from othello.wrapper import OthelloWrapper
from othello.config import APP_SAVE_DIR
from tbs.managers import ReplayManager, UpdateManager


class OthelloReplayManager(ReplayManager):
    cls_wrapper = OthelloWrapper
    base_save_dir = APP_SAVE_DIR


class OthelloUpdateManager(UpdateManager):
    cls_wrapper = OthelloWrapper
    base_save_dir = APP_SAVE_DIR
