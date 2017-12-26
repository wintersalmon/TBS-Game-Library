from tic_tac_toe import TicTacToe
from tic_tac_toe_draw_handler import TicTacToeDrawHandler
from tic_tac_toe_event_handler import TicTacToeEventHandler


class TicTacToeManager(object):
    def __init__(self, player_one, player_two, rows, cols):
        self.game = TicTacToe(player_one, player_two, rows, cols)
        self.events = list()
        self.event_handler = TicTacToeEventHandler(self.game, self.events)
        self.draw_handler = TicTacToeDrawHandler(self.game)

    def update(self, event):
        self.event_handler.update(event)

    def draw(self):
        self.draw_handler.draw()
