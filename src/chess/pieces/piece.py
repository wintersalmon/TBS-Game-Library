from chess.pieces.base import BaseChessPiece
from core.error import InvalidValueError
from core.utils import SerializableMixin, ImmutableMixin


class ChessPiece(BaseChessPiece, ImmutableMixin, SerializableMixin):
    __slots__ = ('_piece', '_color')

    def __init__(self, color, piece):
        if self.is_color(color):
            self._color = color
        else:
            raise InvalidValueError('invalid color value ({})'.format(color))

        if self.is_piece(piece):
            self._piece = piece
        else:
            raise InvalidValueError('invalid piece value ({})'.format(piece))

    @classmethod
    def decode(cls, **kwargs):
        color = kwargs['color']
        piece = kwargs['piece']
        return cls(color=color, piece=piece)

    def encode(self):
        return {
            'color': self._color,
            'piece': self._piece,
        }

    @property
    def value(self):
        return self._piece & self._color

    @property
    def color(self):
        return self.PIECE_COLORS[self._color]

    @property
    def piece(self):
        return self.PIECE_NAMES[self._piece]

    @property
    def fullname(self):
        return '{}{}'.format(self.color, self.piece)

    @property
    def nickname(self):
        nickname = self.PIECE_NICKNAMES[self._piece]
        if self._color == self.WHITE:
            return nickname.upper()
        else:
            return nickname.lower()

    @property
    def pathfinder(self):
        return self.PIECE_PATH_FINDERS[self._color][self._piece]

    def search_valid_destinations(self, board, src):
        return self.pathfinder.search_valid_positions(board, src)

    def is_valid_destination(self, board, src, dst):
        return dst in self.search_valid_destinations(board, src)

    def __repr__(self):
        return self.nickname


class ChessPieceWhitePawn(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.PAWN)


class ChessPieceWhiteRook(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.ROOK)


class ChessPieceWhiteBishop(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.BISHOP)


class ChessPieceWhiteKnight(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.KNIGHT)


class ChessPieceWhiteQueen(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.QUEEN)


class ChessPieceWhiteKing(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.KING)


class ChessPieceBlackPawn(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.PAWN)


class ChessPieceBlackRook(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.ROOK)


class ChessPieceBlackBishop(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.BISHOP)


class ChessPieceBlackKnight(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.KNIGHT)


class ChessPieceBlackQueen(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.QUEEN)


class ChessPieceBlackKing(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.KING)
