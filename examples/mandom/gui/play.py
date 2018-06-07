from kivy.app import App

from mandom.gui.mandom import Mandom
from mandom.managers import MandomUpdateManager


class MandomPlay(Mandom):
    def __init__(self, manager, **kwargs):
        super(MandomPlay, self).__init__(manager.wrapper.game, **kwargs)
        self.manager = manager

    def on_touch_down(self, touch):
        pass
        #
        # for tile in self.board.children[:]:
        #     if tile.collide_point(*touch.pos):
        #         try:
        #             row = tile.row
        #             col = tile.col
        #             event = PlayerPlacementEvent.create(game=self.game, row=row, col=col)
        #             self.manager.update(event)
        #         except ApiError as e:
        #             print(e)
        #             return False
        #         else:
        #             return True


class MandomApp(App):
    def build(self):
        settings = {
            'player_names': ['player_{}'.format(i) for i in range(4)]
        }
        manager = MandomUpdateManager.create(**settings)
        game = MandomPlay(manager=manager)
        return game


GameApp = MandomApp
