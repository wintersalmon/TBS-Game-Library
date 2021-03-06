from othello.board import OthelloBoard
from othello.status import OthelloStatus
from tbs.game import Game
from tbs.player import Player


class OthelloGame(Game):
    def __init__(self, players, *, board=None, status=None):
        self.players = players
        self.board = OthelloBoard() if board is None else board
        self.status = OthelloStatus() if status is None else status

    def encode(self):
        return {
            'players': [player.encode() for player in self.players],
            'board': self.board.encode(),
            'status': self.status.encode()
        }

    @classmethod
    def decode(cls, **kwargs):
        players = [Player.decode(**p_data) for p_data in kwargs['players']]
        board = OthelloBoard.decode(**kwargs['board'])
        status = OthelloStatus.decode(**kwargs['status'])

        return cls(players=players, board=board, status=status)

    @classmethod
    def create(cls, **kwargs):
        players = [Player(p) for p in kwargs['player_names']]
        return cls(players=players)
