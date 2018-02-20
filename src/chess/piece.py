from chess.pathfinders import *
from core.error import InvalidValueError
from core.utils import SerializableMixin, ImmutableMixin

COLOR = 0
NAME = 1
PATHFINDER = 2

PIECE_COLOR_WHITE = 'White'
PIECE_COLOR_BLACK = 'Black'

PIECE_NAME_PAWN = 'Pawn'
PIECE_NAME_ROOK = 'Rook'
PIECE_NAME_BISHOP = 'Bishop'
PIECE_NAME_KNIGHT = 'Knight'
PIECE_NAME_QUEEN = 'Queen'
PIECE_NAME_KING = 'King'

PIECE_KEY_WHITE_PAWN = 'P'
PIECE_KEY_WHITE_ROOK = 'R'
PIECE_KEY_WHITE_BISHOP = 'B'
PIECE_KEY_WHITE_KNIGHT = 'N'
PIECE_KEY_WHITE_QUEEN = 'Q'
PIECE_KEY_WHITE_KING = 'K'

PIECE_KEY_BLACK_PAWN = 'p'
PIECE_KEY_BLACK_ROOK = 'r'
PIECE_KEY_BLACK_BISHOP = 'b'
PIECE_KEY_BLACK_KNIGHT = 'n'
PIECE_KEY_BLACK_QUEEN = 'q'
PIECE_KEY_BLACK_KING = 'k'

CHESS_PIECES = {
    PIECE_KEY_WHITE_PAWN: (PIECE_COLOR_WHITE, PIECE_NAME_PAWN, ChessWhitePawnPathFinder()),
    PIECE_KEY_WHITE_ROOK: (PIECE_COLOR_WHITE, PIECE_NAME_ROOK, ChessRookPathFinder()),
    PIECE_KEY_WHITE_BISHOP: (PIECE_COLOR_WHITE, PIECE_NAME_BISHOP, ChessBishopPathFinder()),
    PIECE_KEY_WHITE_KNIGHT: (PIECE_COLOR_WHITE, PIECE_NAME_KNIGHT, ChessKnightPathFinder()),
    PIECE_KEY_WHITE_QUEEN: (PIECE_COLOR_WHITE, PIECE_NAME_QUEEN, ChessQueenPathFinder()),
    PIECE_KEY_WHITE_KING: (PIECE_COLOR_WHITE, PIECE_NAME_KING, ChessKingPathFinder()),

    PIECE_KEY_BLACK_PAWN: (PIECE_COLOR_BLACK, PIECE_NAME_PAWN, ChessBlackPawnPathFinder()),
    PIECE_KEY_BLACK_ROOK: (PIECE_COLOR_BLACK, PIECE_NAME_ROOK, ChessRookPathFinder()),
    PIECE_KEY_BLACK_BISHOP: (PIECE_COLOR_BLACK, PIECE_NAME_BISHOP, ChessBishopPathFinder()),
    PIECE_KEY_BLACK_KNIGHT: (PIECE_COLOR_BLACK, PIECE_NAME_KNIGHT, ChessKnightPathFinder()),
    PIECE_KEY_BLACK_QUEEN: (PIECE_COLOR_BLACK, PIECE_NAME_QUEEN, ChessQueenPathFinder()),
    PIECE_KEY_BLACK_KING: (PIECE_COLOR_BLACK, PIECE_NAME_KING, ChessKingPathFinder()),
}


class ChessPiece(ImmutableMixin, SerializableMixin):
    __slots__ = ('nickname', 'color', 'fullname', 'pathfinder')

    def __init__(self, nickname):
        if nickname not in CHESS_PIECES.keys():
            raise InvalidValueError('invalid piece value({})'.format(nickname))
        self.nickname = nickname
        self.color = CHESS_PIECES[nickname][COLOR]
        self.name = CHESS_PIECES[nickname][NAME]
        self.fullname = self.color + self.name
        self.pathfinder = CHESS_PIECES[nickname][PATHFINDER]

    def search_valid_destinations(self, board, src):
        return self.pathfinder.search_valid_positions(board, src)

    def is_valid_destination(self, board, src, dst):
        return dst in self.search_valid_destinations(board, src)

    def encode(self):
        return self.nickname

    @classmethod
    def decode(cls, nickname):
        return cls(nickname=nickname)

    def __str__(self):
        return self.nickname

    def __eq__(self, other):
        if isinstance(other, ChessPiece):
            return self.nickname == other.nickname
        elif isinstance(other, str):
            return self.nickname == other
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)
