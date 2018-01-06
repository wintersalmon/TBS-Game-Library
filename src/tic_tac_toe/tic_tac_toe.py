from tic_tac_toe.board import TTTBoard
from core.player import Player


class TicTacToe(object):
    def __init__(self, player_one, player_two, rows, cols):
        self.players = dict()
        self.players[player_one] = Player(player_one)
        self.players[player_two] = Player(player_two)
        self.player_names = (player_one, player_two)
        self.board = TTTBoard(rows=rows, cols=cols)
        self.turn_count = 0
        self.status = True

    def __repr__(self):
        players_fmt = 'players: {}'.format(list(self.players.keys()))
        return '\n'.join((players_fmt, str(self.board)))

    def get_turn_player_name(self):
        return self.player_names[self.turn_count % 2]
