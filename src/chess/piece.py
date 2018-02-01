from chess.paths.finder import ChessBishopPathFinder, ChessKingPathFinder
from chess.paths.finder import ChessBlackPawnPathFinder
from chess.paths.finder import ChessKnightPathFinder
from chess.paths.finder import ChessQueenPathFinder
from chess.paths.finder import ChessRookPathFinder
from chess.paths.finder import ChessWhitePawnPathFinder
from core.utils import SerializableMixin, ImmutableMixin


class BaseChessPiece(object):
    # PIECE CODES
    BLANK = 0

    PAWN = 2 ** 1
    ROOK = 2 ** 2
    BISHOP = 2 ** 3
    KNIGHT = 2 ** 4
    QUEEN = 2 ** 5
    KING = 2 ** 6

    BLACK = 2 ** 9
    WHITE = 2 ** 10

    # PIECE VERIFIER
    COLOR_BIT = BLACK | WHITE
    PIECE_BIT = PAWN | ROOK | BISHOP | KNIGHT | QUEEN | KING

    ALL_COLORS = (BLACK, WHITE)
    ALL_PIECES = (PAWN, ROOK, BISHOP, KNIGHT, QUEEN, KING)

    # PIECE NAMES
    PIECE_COLORS = {
        BLACK: 'Black',
        WHITE: 'White',
    }

    PIECE_NAMES = {
        PAWN: 'Pawn',
        ROOK: 'Rook',
        BISHOP: 'Bishop',
        KNIGHT: 'Knight',
        QUEEN: 'Queen',
        KING: 'King',
    }

    PIECE_NICKNAMES = {
        PAWN: 'P',
        ROOK: 'R',
        BISHOP: 'B',
        KNIGHT: 'N',
        QUEEN: 'Q',
        KING: 'K',
    }

    # PIECE ACTIONS
    PIECE_PATH_FINDERS = {
        BLACK: {
            PAWN: ChessBlackPawnPathFinder(),
            ROOK: ChessRookPathFinder(),
            BISHOP: ChessBishopPathFinder(),
            KNIGHT: ChessKnightPathFinder(),
            QUEEN: ChessQueenPathFinder(),
            KING: ChessKingPathFinder(),
        },
        WHITE: {
            PAWN: ChessWhitePawnPathFinder(),
            ROOK: ChessRookPathFinder(),
            BISHOP: ChessBishopPathFinder(),
            KNIGHT: ChessKnightPathFinder(),
            QUEEN: ChessQueenPathFinder(),
            KING: ChessKingPathFinder(),
        }
    }

    @classmethod
    def get_color_value(cls, tile):
        return tile & cls.COLOR_BIT

    @classmethod
    def get_piece_value(cls, tile):
        return tile & cls.PIECE_BIT

    @classmethod
    def is_color(cls, value):
        return cls.get_color_value(value) in cls.ALL_COLORS

    @classmethod
    def is_piece(cls, value):
        return cls.get_piece_value(value) in cls.ALL_PIECES

    @classmethod
    def is_tile(cls, value):
        return cls.is_color(value) and cls.is_piece(value)


class ChessPiece(BaseChessPiece, ImmutableMixin, SerializableMixin):
    __slots__ = ('_value', '_piece', '_color')

    def __init__(self, value):
        if not self.is_tile(value):
            raise ValueError('invalid value')

        self._value = value
        self._color = self.get_color_value(value)
        self._piece = self.get_piece_value(value)

    @classmethod
    def decode(cls, **kwargs):
        value = kwargs['value']
        return cls(value=value)

    def encode(self):
        return {
            'value': self._value
        }

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

    def search_valid_destinations(self, board, src):
        pathfinder = self.PIECE_PATH_FINDERS[self._color][self._piece]
        return pathfinder.search_valid_positions(board, src)

    def can_move_to(self, board, src, dst):
        valid_destinations = self.search_valid_destinations(board, src)
        return dst in valid_destinations

    def __repr__(self):
        return self.nickname


class ChessPieceWhitePawn(ChessPiece):
    def __init__(self):
        super().__init__(self.WHITE | self.PAWN)


class ChessPieceWhiteRook(ChessPiece):
    def __init__(self):
        super().__init__(self.WHITE | self.ROOK)


class ChessPieceWhiteBishop(ChessPiece):
    def __init__(self):
        super().__init__(self.WHITE | self.BISHOP)


class ChessPieceWhiteKnight(ChessPiece):
    def __init__(self):
        super().__init__(self.WHITE | self.KNIGHT)


class ChessPieceWhiteQueen(ChessPiece):
    def __init__(self):
        super().__init__(self.WHITE | self.QUEEN)


class ChessPieceWhiteKing(ChessPiece):
    def __init__(self):
        super().__init__(self.WHITE | self.KING)


class ChessPieceBlackPawn(ChessPiece):
    def __init__(self):
        super().__init__(self.BLACK | self.PAWN)


class ChessPieceBlackRook(ChessPiece):
    def __init__(self):
        super().__init__(self.BLACK | self.ROOK)


class ChessPieceBlackBishop(ChessPiece):
    def __init__(self):
        super().__init__(self.BLACK | self.BISHOP)


class ChessPieceBlackKnight(ChessPiece):
    def __init__(self):
        super().__init__(self.BLACK | self.KNIGHT)


class ChessPieceBlackQueen(ChessPiece):
    def __init__(self):
        super().__init__(self.BLACK | self.QUEEN)


class ChessPieceBlackKing(ChessPiece):
    def __init__(self):
        super().__init__(self.BLACK | self.KING)
