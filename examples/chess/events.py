from chess.game import ChessGame
from chess.piece import ChessPiece
from tbs.error import EventCreationFailedError
from tbs.event import Event
from tbs.position import Position


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
        encoded_properties = {
            'pos_src': self.pos_src.encode(),
            'pos_dst': self.pos_dst.encode(),
            'piece_src': self.piece_src.encode(),
        }

        if self.piece_dst is not None:
            encoded_properties['piece_dst'] = self.piece_dst.encode()

        return encoded_properties

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'pos_src': Position.decode(**kwargs['pos_src']),
            'pos_dst': Position.decode(**kwargs['pos_dst']),
            'piece_src': ChessPiece.decode(kwargs['piece_src']),
        }

        if 'piece_dst' in kwargs:
            decoded_kwargs['piece_dst'] = ChessPiece.decode(kwargs['piece_dst'])

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, *, game, **kwargs):
        # retrieve basic arguments or throw error
        if not isinstance(game, ChessGame):
            raise EventCreationFailedError('invalid data type game(ChessGame)')
        pos_src = cls.get_argument_or_raise_error(kwargs, 'pos_src')
        pos_dst = cls.get_argument_or_raise_error(kwargs, 'pos_dst')

        piece_src = game.board.get(pos_src.row, pos_src.col)
        piece_dst = game.board.get(pos_dst.row, pos_dst.col)

        if not isinstance(piece_src, ChessPiece):
            raise EventCreationFailedError('source position cannot be empty ({})'.format(pos_src))

        if not isinstance(piece_dst, ChessPiece):
            piece_dst = None

        if piece_src.is_valid_destination(game.board, pos_src, pos_dst):
            return MoveChessPieceEvent(pos_src=pos_src, pos_dst=pos_dst, piece_src=piece_src, piece_dst=piece_dst)
        else:
            raise EventCreationFailedError(
                'cannot create event with flowing arguments ({}, {})'.format(pos_src, pos_dst))
