from chess.game import ChessGame
from chess.piece import ChessPiece
from core.error import EventCreationFailedError, InvalidPositionError
from core.event import Event
from core.position import Position


class MoveChessPieceEvent(Event):
    def __init__(self, pos_src, pos_dst, piece_src, piece_dst=None):
        # verify data type
        if not isinstance(pos_src, Position):
            raise ValueError('invalid data type pos_src(Position)')

        if not isinstance(pos_dst, Position):
            raise ValueError('invalid data type pos_dst(Position)')

        if not isinstance(piece_src, ChessPiece):
            raise ValueError('invalid data type piece_src(ChessPiece)')

        if (piece_dst is not None) and (not isinstance(piece_dst, ChessPiece)):
            raise ValueError('invalid data type piece_dst(ChessPiece)')

        self.pos_src = pos_src
        self.pos_dst = pos_dst
        self.piece_src = piece_src
        self.piece_dst = piece_dst

    def update(self, game):
        if self.piece_dst is not None:
            game.board.reset_tile(self.pos_dst.row, self.pos_dst.col)
        game.board.reset_tile(self.pos_src.row, self.pos_src.col)
        game.board.set(self.pos_dst.row, self.pos_dst.col, self.piece_src)

        game.turn_count += 1

    def rollback(self, game):
        game.board.reset_tile(self.pos_dst.row, self.pos_dst.col)
        game.board.set(self.pos_src.row, self.pos_src.col, self.piece_src)
        if self.piece_dst is not None:
            game.board.set(self.pos_dst.row, self.pos_dst.col, self.piece_dst)

        game.turn_count -= 1

    def encode(self):
        return {
            'pos_src': self.pos_src.encode(),
            'pos_dst': self.pos_dst.encode(),
            'piece_src': self.piece_src.encode(),
            'piece_dst': self.piece_dst.encode() if self.piece_dst else self.piece_dst,
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'pos_src': Position.decode(**kwargs['pos_src']),
            'pos_dst': Position.decode(**kwargs['pos_dst']),
            'piece_src': ChessPiece.decode(**kwargs['piece_src']),
            'piece_dst': ChessPiece.decode(**kwargs['piece_dst']) if kwargs['piece_dst'] else None,
        }
        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, *, game, **kwargs):
        # retrieve basic arguments or throw error
        if not isinstance(game, ChessGame):
            raise EventCreationFailedError('invalid data type game(ChessGame)')
        pos_src = cls.get_argument_or_raise_error(kwargs, 'pos_src')
        pos_dst = cls.get_argument_or_raise_error(kwargs, 'pos_dst')

        # retrieve extra arguments or throw errors
        try:
            if game.board.is_set(pos_src.row, pos_src.col):
                piece_src = game.board.get(pos_src.row, pos_src.col)
            else:
                piece_src = None
            if game.board.is_set(pos_dst.row, pos_dst.col):
                piece_dst = game.board.get(pos_dst.row, pos_dst.col)
            else:
                piece_dst = None

            game.board.can_move(pos_src, pos_dst)

        except InvalidPositionError as e:
            raise EventCreationFailedError(e)

        else:
            return MoveChessPieceEvent(pos_src=pos_src, pos_dst=pos_dst, piece_src=piece_src, piece_dst=piece_dst)
