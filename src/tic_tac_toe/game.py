from core.player import Player
from core.utils import SerializableMixin
from tic_tac_toe.board import TTTBoard
from tic_tac_toe.status import TTTStatus


class TicTacToeGame(SerializableMixin):
    def __init__(self, players, *, board=None, status=None):
        self.players = players
        self.board = TTTBoard() if board is None else board
        self.status = TTTStatus() if status is None else status

    def encode(self):
        return {
            'players': [player.encode() for player in self.players],
            'board': self.board.encode(),
            'status': self.status.encode()
        }

    @classmethod
    def decode(cls, **kwargs):
        players = [Player.decode(**p_data) for p_data in kwargs['players']]
        board = TTTBoard.decode(**kwargs['board'])
        status = TTTStatus.decode(**kwargs['status'])

        return cls(players=players, board=board, status=status)
