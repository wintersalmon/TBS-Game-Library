from player import Player
from board import Board


class Othello(object):
    def __init__(self, player_one, player_two):
        self.players = dict()
        self.players[player_one] = Player(player_one)
        self.players[player_two] = Player(player_two)
        self.board = Board()
        self.player_names = (player_one, player_two)
        self.turn_count = 0
        self.status = True

    def get_turn_player_name(self):
        return ''

    def __bool__(self):
        return self.status
