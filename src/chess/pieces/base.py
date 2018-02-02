from chess.pieces.pathfinder import ChessBishopPathFinder, ChessKingPathFinder, ChessBlackPawnPathFinder, \
    ChessKnightPathFinder, ChessQueenPathFinder, ChessRookPathFinder, ChessWhitePawnPathFinder


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
