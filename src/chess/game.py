from chess.board import ChessBoard
from core.player import Player
from core.utils import Serializable


class ChessGame(Serializable):
    def __init__(self, *, players, board, turn_count, status):
        self.players = players
        self.board = board
        self.turn_count = turn_count
        self.status = status

    def __repr__(self):
        players_repr = 'players: {}'.format([player.name for player in self.players])
        board_repr = repr(self.board)
        reprs = (players_repr, board_repr)
        return '\n'.join(reprs)

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
