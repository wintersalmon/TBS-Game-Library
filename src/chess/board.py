from chess.piece import ChessPiece
from core.board import Board
from core.error import InvalidPositionError, InvalidValueError


class ChessBoard(Board):
    MARKER_INIT = -1
    PIECE_BLACK = 'BLACK'
    PIECE_WHITE = 'WHITE'
    PIECE_KING = 'KING'
    PIECE_QUEEN = 'QUEEN'
    PIECE_ROOK = 'ROOK'
    PIECE_BISHOP = 'BISHOP'
    PIECE_KNIGHT = 'KNIGHT'
    PIECE_PAWN = 'PAWN'

    INIT_PIECE_ORDER = [
        PIECE_ROOK,
        PIECE_KNIGHT,
        PIECE_BISHOP,
        PIECE_QUEEN,
        PIECE_KING,
        PIECE_BISHOP,
        PIECE_KNIGHT,
        PIECE_ROOK,
    ]

    def __init__(self, tiles=None):
        if tiles is None:
            super().__init__(8, 8, init_value=self.MARKER_INIT)
            self._init_chess_pieces()
        else:
            super().__init__(8, 8, init_value=self.MARKER_INIT, tiles=tiles)

    def _init_chess_pieces(self):
        for col in range(8):
            self.tiles[0][col] = ChessPiece(name=self.INIT_PIECE_ORDER[col], color=self.PIECE_WHITE)
            self.tiles[1][col] = ChessPiece(name=self.PIECE_PAWN, color=self.PIECE_WHITE)
            self.tiles[6][col] = ChessPiece(name=self.PIECE_PAWN, color=self.PIECE_BLACK)
            self.tiles[7][col] = ChessPiece(name=self.INIT_PIECE_ORDER[col], color=self.PIECE_BLACK)

    def set(self, row, col, value):
        if isinstance(value, ChessPiece):
            super().set(row, col, value)
        else:
            raise InvalidValueError('invalid value to set {}'.format(value))

    def can_move(self, src_pos, dst_pos):
        if not self.is_set(src_pos.row, src_pos.col):
            raise InvalidPositionError('from position({}) should not be empty'.format(src_pos))

        # TODO: check whether src_pos piece can move to dst_pos
        # raise InvalidPositionError
        # 'from position({}), to position({}) cannot be reached'.format(src_pos, dst_pos)

        # TODO: check whether there is not obstacles in between src_pos and dst_pos
        # raise InvalidPositionError
        # 'from position({}), to position({}) should not have obstacles in between'.format(src_pos, dst_pos)

        if self.is_set(dst_pos.row, dst_pos.col):
            if self.get(src_pos.row, src_pos.col).color == self.get(dst_pos.row, dst_pos.col).color:
                raise InvalidPositionError(
                    'from position({}), to position({}) should not have same color'.format(src_pos, dst_pos))

        return True

    def encode(self):
        encoded_tiles = list()
        for rows in self.tiles:
            encoded_rows = list()
            for piece in rows:
                if piece is self.init_value:
                    encoded_rows.append(self.init_value)
                else:
                    encoded_rows.append(piece.encode())
            encoded_tiles.append(encoded_rows)

        return {'tiles': encoded_tiles}

    @classmethod
    def decode(cls, **kwargs):
        decoded_tiles = list()
        for rows in kwargs['tiles']:
            decoded_rows = list()
            for piece in rows:
                try:
                    value = ChessPiece.decode(**piece)
                except TypeError:
                    value = piece
                decoded_rows.append(value)
            decoded_tiles.append(decoded_rows)

        return cls(tiles=decoded_tiles)

    def __repr__(self):
        lines = list()
        first_line = '   0  1  2  3  4  5  6  7'
        lines.append(first_line)
        for r, rows in enumerate(self.tiles):
            line = list()
            for piece in rows:
                marker = self.__repr_piece(piece)
                line.append('{}  '.format(marker))
            line.insert(0, '{}  '.format(r))
            lines.append(''.join(line))

        return '\n'.join(lines)

    def __repr_piece(self, piece):
        if isinstance(piece, ChessPiece):
            if piece.name == self.PIECE_KNIGHT:
                marker = 'N'
            else:
                marker = piece.name[0]
            if piece.color == self.PIECE_BLACK:
                marker = marker.lower()

        else:
            marker = '.'

        return '{}'.format(marker)
