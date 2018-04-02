import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

SAVE_DIR_ROOT = os.path.join(ROOT_DIR, 'save')
SAVE_DIR = {
    'tic_tac_toe': os.path.join(SAVE_DIR_ROOT, 'tic_tac_toe'),
    'othello': os.path.join(SAVE_DIR_ROOT, 'othello'),
    'chess': os.path.join(SAVE_DIR_ROOT, 'chess'),
}

FT_SCRIPT_DIR = os.path.join(ROOT_DIR, 'ft_script')
