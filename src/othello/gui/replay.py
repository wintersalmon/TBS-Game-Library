from kivy.app import App

from core.gui import GUIReplay
from othello.managers import OthelloReplayManager
from .othello import Othello


class OthelloApp(App):
    def build(self):
        manager = OthelloReplayManager.load('b_01')
        game = GUIReplay(Othello, manager)
        return game


GameApp = OthelloApp
