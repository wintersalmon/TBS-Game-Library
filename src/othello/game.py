from core.player import Player
from core.utils import Serializable
from othello.board import OthelloBoard


class OthelloGame(Serializable):
    def __init__(self, players, *, board=None, turn_count=0, status=True):
        self.players = players
        self.board = OthelloBoard() if board is None else board
        self.turn_count = turn_count if turn_count >= 0 else 0
        self.status = status

    def get_turn_player_number(self):
        return self.turn_count % len(self.players)

    def __bool__(self):
        return self.status

    def encode(self):
        return {
            'players': [player.encode() for player in self.players],
            'board': self.board.encode(),
            'turn_count': self.turn_count,
            'status': self.status
        }

    @classmethod
    def decode(cls, **kwargs):
        players = [Player.decode(**p_data) for p_data in kwargs['players']]
        board = OthelloBoard.decode(**kwargs['board'])
        turn_count = kwargs['turn_count']
        status = kwargs['status']

        return cls(players=players, board=board, turn_count=turn_count, status=status)
