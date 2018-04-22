from kivy.app import App

from tbs.gui import GUIReplay
from tic_tac_toe.gui.tictactoe import TicTacToe
from tic_tac_toe.managers import TicTacToeReplayManager


class TicTacToeApp(App):
    def build(self):
        manager = TicTacToeReplayManager.load('first')
        return GUIReplay(TicTacToe, manager)


GameApp = TicTacToeApp
