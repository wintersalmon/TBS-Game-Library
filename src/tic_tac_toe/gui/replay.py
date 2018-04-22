from kivy.app import App

from core.gui import GUIReplay
from tic_tac_toe.managers import TicTacToeReplayManager
from .tictactoe import TicTacToe


class TicTacToeApp(App):
    def build(self):
        manager = TicTacToeReplayManager.load('first')
        return GUIReplay(TicTacToe, manager)


GameApp = TicTacToeApp
