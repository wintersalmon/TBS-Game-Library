import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

SAVE_DIR = os.path.join(ROOT_DIR, 'save')
TTT_SAVE_DIR = os.path.join(SAVE_DIR, 'tic_tac_toe')
OTHELLO_SAVE_DIR = os.path.join(SAVE_DIR, 'othello')
CHESS_SAVE_DIR = os.path.join(SAVE_DIR, 'chess')

FT_SCRIPT_DIR = os.path.join(ROOT_DIR, 'ft_script')
