from kivy.app import App

from core.error import ApiError
from othello.events import PlayerPlacementEvent
from othello.managers import OthelloUpdateManager
from .othello import Othello


class OthelloPlay(Othello):
    def __init__(self, manager, **kwargs):
        super(OthelloPlay, self).__init__(manager.wrapper.game, **kwargs)
        self.manager = manager

    def on_touch_down(self, touch):
        if not bool(self.game.status):
            return False

        for tile in self.board.children[:]:
            if tile.collide_point(*touch.pos):
                try:
                    row = tile.row
                    col = tile.col
                    event = PlayerPlacementEvent.create(game=self.game, row=row, col=col)
                    self.manager.update(event)
                except ApiError as e:
                    print(e)
                    return False
                else:
                    return True


class OthelloApp(App):
    def build(self):
        settings = {'player_names': ['tom', 'jerry']}
        manager = OthelloUpdateManager.create(**settings)
        game = OthelloPlay(manager=manager)
        return game


GameApp = OthelloApp
