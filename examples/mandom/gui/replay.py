from kivy.app import App

from mandom.gui.mandom import Mandom
from mandom.managers import MandomReplayManager
from tbs.gui import GUIReplay


class MandomApp(App):

    def build(self):
        manager = MandomReplayManager.load('first')
        return GUIReplay(Mandom, manager)


GameApp = MandomApp
