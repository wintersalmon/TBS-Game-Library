from core.managers import ReplayManager, UpdateManager
from settings import SAVE_DIR
from .wrapper import OthelloWrapper


class OthelloReplayManager(ReplayManager):
    cls_wrapper = OthelloWrapper
    base_save_dir = SAVE_DIR['othello']


class OthelloUpdateManager(UpdateManager):
    cls_wrapper = OthelloWrapper
    base_save_dir = SAVE_DIR['othello']
