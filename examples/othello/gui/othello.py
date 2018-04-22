from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ColorProperty, NumericProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from othello.wrapper import OthelloWrapper


class OthelloTile(Widget):
    color = ColorProperty(None)
    marker = NumericProperty(None)
    row = NumericProperty(None)
    col = NumericProperty(None)

    def __init__(self, marker, row, col, **kwargs):
        super(OthelloTile, self).__init__(**kwargs)
        self.marker = marker
        self.row = row
        self.col = col

    def on_marker(self, instance, marker):
        if marker == 1:
            self.opacity = 1
            self.color = (0, 0, 0, 1)

        elif marker == 2:
            self.opacity = 1
            self.color = (1, 1, 1, 1)

        elif marker < 0:
            alpha = (self.marker * -1) / 10
            alpha = 1 if alpha > 1 else alpha
            self.opacity = 1
            self.color = (1, 0, 0, alpha)

        else:
            self.opacity = 0


class Othello(GridLayout):
    player1 = StringProperty('NO_NAME')
    player2 = StringProperty('NO_NAME')
    status = StringProperty('NO STATUS')
    score = StringProperty('NO SCORE')
    board = ObjectProperty(None)

    def __init__(self, game, **kwargs):
        super(Othello, self).__init__(**kwargs)
        self.cols = 1
        self.game = game

        self.player1 = self.game.players[0].name
        self.player2 = self.game.players[1].name
        self.status = 'Running' if bool(self.game.status) else 'Stopped'
        self.score = 'Black({:2}) vs White({:2})'.format(*self.game.board.count)

        for r, rows in enumerate(self.game.board.tiles):
            for c, marker in enumerate(rows):
                tile = OthelloTile(marker=marker, row=r, col=c)
                self.board.add_widget(tile)

        Clock.schedule_interval(self.draw, 1.0 / 30.0)

    def draw(self, dt):
        # update status
        self.status = 'Running' if bool(self.game.status) else 'Stopped'
        self.score = 'Black({:2}) vs White({:2})'.format(*self.game.board.count)

        # update tiles
        turn_player = self.game.status.player
        for tile in self.board.children[:]:
            row = tile.row
            col = tile.col
            if self.game.board.is_set(row, col):
                marker = self.game.board.get(row, col)
            else:
                flips = self.game.board.find_flip_positions(row, col, turn_player)
                flip_count = len(flips)
                if flip_count:
                    marker = flip_count * -1
                else:
                    marker = 0
            tile.marker = marker


class OthelloApp(App):
    def build(self):
        settings = {'player_names': ['tom', 'jerry']}
        wrapper = OthelloWrapper.create(**settings)
        game = Othello(game=wrapper.game)
        return game


if __name__ == '__main__':
    OthelloApp().run()
