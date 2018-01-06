from tic_tac_toe.tic_tac_toe import TicTacToe
from tic_tac_toe.tic_tac_toe_draw_handler import TicTacToeDrawHandler
from tic_tac_toe.tic_tac_toe_event_handler import TicTacToeEventHandler
from collections import MutableSequence


class TicTacToeManager(object):
    def __init__(self, game, events):
        if not isinstance(game, TicTacToe):
            raise ValueError('invalid type game (TicTacToe)')

        if not isinstance(events, MutableSequence):
            raise ValueError('invalid type events (MutableSequence)')

        self.game = game
        self.events = events
        self.event_handler = TicTacToeEventHandler(self.game, self.events)
        self.draw_handler = TicTacToeDrawHandler(self.game)

    def is_running(self):
        return self.game.status

    def update(self, event):
        self.event_handler.update(event)

    def draw(self):
        self.draw_handler.draw()

    @classmethod
    def create(cls, player_one, player_two, rows, cols):
        game = TicTacToe(player_one, player_two, rows, cols)
        events = list()
        return cls(game, events)
