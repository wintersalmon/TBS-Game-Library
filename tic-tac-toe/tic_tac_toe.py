from board import Board
from player import Player


class TicTacToe(object):
    def __init__(self, player_one, player_two, rows, cols):
        players = {
            player_one: Player(player_one),
            player_two: Player(player_two)
        }
        board = Board(rows=rows, cols=cols)

        self.players = players
        self.board = board
        self.status = True

    def __repr__(self):
        players_fmt = 'players: {}'.format(list(self.players.keys()))
        return '\n'.join((players_fmt, str(self.board)))
