from kivy.app import App

from core.error import ApiError
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.managers import TicTacToeUpdateManager
from .tictactoe import TicTacToe


class TicTacToePlay(TicTacToe):
    def __init__(self, manager, **kwargs):
        super(TicTacToePlay, self).__init__(manager.wrapper.game, **kwargs)
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


class TicTacToeApp(App):
    def build(self):
        settings = {'player_names': ['tom', 'jerry']}
        manager = TicTacToeUpdateManager.create(**settings)
        game = TicTacToePlay(manager=manager)
        return game


GameApp = TicTacToeApp
