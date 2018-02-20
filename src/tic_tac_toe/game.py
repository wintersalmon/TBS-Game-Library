from tic_tac_toe.board import TTTBoard
from core.player import Player
from core.utils import SerializableMixin


class TicTacToeGame(SerializableMixin):
    def __init__(self, players, *, board=None, turn_count=0, status=True):
        self.players = players
        self.board = TTTBoard() if board is None else board
        self.turn_count = turn_count if turn_count >= 0 else 0
        self.status = status

    def __str__(self):
        players_fmt = 'players: {}'.format([player.name for player in self.players])
        return '\n'.join((players_fmt, str(self.board)))

    def get_turn_player_name(self):
        total_players = len(self.players)
        cur_player_number = self.turn_count % total_players
        return self.players[cur_player_number].name

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
        board = TTTBoard.decode(**kwargs['board'])
        turn_count = kwargs['turn_count']
        status = kwargs['status']

        return cls(players=players, board=board, turn_count=turn_count, status=status)
