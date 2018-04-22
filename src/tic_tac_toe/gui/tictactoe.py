from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ColorProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from tic_tac_toe.wrapper import TicTacToeWrapper


class TicTacToeTile(Label):
    color = ColorProperty(None)
    marker = NumericProperty(None)
    row = NumericProperty(None)
    col = NumericProperty(None)

    def __init__(self, marker, row, col, **kwargs):
        super(TicTacToeTile, self).__init__(**kwargs)
        self.marker = marker
        self.row = row
        self.col = col

    def on_marker(self, instance, marker):
        if marker == 0:
            self.color = (0, 0, 0, 1)

        elif marker == 1:
            self.color = (1, 1, 1, 1)

        else:
            self.color = (1, 0, 0, 0.25)


class TicTacToe(GridLayout):
    player1 = StringProperty('NO_NAME')
    player2 = StringProperty('NO_NAME')
    status = StringProperty('NO STATUS')
    score = StringProperty('NO SCORE')
    board = ObjectProperty(None)

    def __init__(self, game, **kwargs):
        super(TicTacToe, self).__init__(**kwargs)
        self.cols = 1
        self.game = game

        self.player1 = self.game.players[0].name
        self.player2 = self.game.players[1].name
        self.status = 'Running' if bool(self.game.status) else 'Stopped'

        for r, rows in enumerate(self.game.board.tiles):
            for c, marker in enumerate(rows):
                tile = TicTacToeTile(marker=marker, row=r, col=c)
                self.board.add_widget(tile)

        Clock.schedule_interval(self.draw, 1.0 / 30.0)

    def draw(self, dt):
        # update status
        self.status = 'Running' if bool(self.game.status) else 'Stopped'

        # update tiles
        for tile in self.board.children[:]:
            row = tile.row
            col = tile.col
            tile.marker = self.game.board.get(row, col)


class TicTacToeApp(App):
    def build(self):
        settings = {'player_names': ['tom', 'jerry']}
        wrapper = TicTacToeWrapper.create(**settings)
        game = TicTacToe(game=wrapper.game)
        return game


if __name__ == '__main__':
    TicTacToeApp().run()
