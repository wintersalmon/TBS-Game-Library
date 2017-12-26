from board import Board
from player import Player


class TicTacToe(object):
    markers = ('O', 'X')

    def __init__(self, player_one, player_two, rows, cols):
        players = {
            player_one: Player(player_one, self.markers[0]),
            player_two: Player(player_two, self.markers[1])
        }
        board = Board(rows=rows, cols=cols)

        self.players = players
        self.board = board

    def __repr__(self):
        lines = list()
        for player in self.players:
            lines.append(str(player))
        lines.append(str(self.board))

        return '\n'.join(lines)
