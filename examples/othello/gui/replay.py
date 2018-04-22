from kivy.app import App

from othello.gui.othello import Othello
from othello.managers import OthelloReplayManager
from tbs.gui import GUIReplay


class OthelloApp(App):
    def build(self):
        manager = OthelloReplayManager.load('b_01')
        game = GUIReplay(Othello, manager)
        return game


GameApp = OthelloApp
