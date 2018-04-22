from chess.board import ChessBoard
from tbs.player import Player
from tbs.utils import SerializableMixin


class ChessGame(SerializableMixin):
    def __init__(self, *, players, board, turn_count, status):
        self.players = players
        self.board = board
        self.turn_count = turn_count
        self.status = status

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
        board = ChessBoard.decode(**kwargs['board'])
        turn_count = kwargs['turn_count']
        status = kwargs['status']

        return cls(players=players, board=board, turn_count=turn_count, status=status)

    @classmethod
    def create(cls, **kwargs):
        players = [Player(name=name) for name in kwargs['player_names']]
        board = ChessBoard()
        turn_count = 0
        status = True

        return cls(players=players, board=board, turn_count=turn_count, status=status)
