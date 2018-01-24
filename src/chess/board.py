from chess.paths.finder import ChessPathFinder
from chess.piece import ChessPiece
from core.board import Board
from core.error import InvalidPositionError, InvalidValueError


class ChessBoard(Board):
    MARKER_INIT = -1

    INIT_PIECE_ORDER = [
        ChessPiece.ROOK,
        ChessPiece.KNIGHT,
        ChessPiece.BISHOP,
        ChessPiece.QUEEN,
        ChessPiece.KING,
        ChessPiece.BISHOP,
        ChessPiece.KNIGHT,
        ChessPiece.ROOK,
    ]

    def __init__(self, tiles=None):
        if tiles is None:
            super().__init__(8, 8, init_value=self.MARKER_INIT)
            self._init_chess_pieces()
        else:
            super().__init__(8, 8, init_value=self.MARKER_INIT, tiles=tiles)
        self.chess_path_finder = ChessPathFinder()

    def _init_chess_pieces(self):
        for col in range(8):
            self.tiles[0][col] = ChessPiece(name=self.INIT_PIECE_ORDER[col], color=ChessPiece.COLOR_WHITE)
            self.tiles[1][col] = ChessPiece(name=ChessPiece.PAWN, color=ChessPiece.COLOR_WHITE)
            self.tiles[6][col] = ChessPiece(name=ChessPiece.PAWN, color=ChessPiece.COLOR_BLACK)
            self.tiles[7][col] = ChessPiece(name=self.INIT_PIECE_ORDER[col], color=ChessPiece.COLOR_BLACK)

    def set(self, row, col, value):
        if isinstance(value, ChessPiece):
            super().set(row, col, value)
        else:
            raise InvalidValueError('invalid value to set {}'.format(value))

    def can_move(self, src_pos, dst_pos):
        if not self.is_set(src_pos.row, src_pos.col):
            raise InvalidPositionError('from position({}) should not be empty'.format(src_pos))

        # TODO : clean up required
        src_piece = self.get(src_pos.row, src_pos.col)
        src_move_paths = list()
        if src_piece.name == 'KING':
            src_move_paths = self.chess_path_finder.select_king_move_positions(src_pos)
        elif src_piece.name == 'QUEEN':
            src_move_paths = self.chess_path_finder.select_queen_move_positions(src_pos)
        elif src_piece.name == 'ROOK':
            src_move_paths = self.chess_path_finder.select_rook_move_positions(src_pos)
        elif src_piece.name == 'BISHOP':
            src_move_paths = self.chess_path_finder.select_bishop_move_positions(src_pos)
        elif src_piece.name == 'KNIGHT':
            src_move_paths = self.chess_path_finder.select_knight_move_positions(src_pos)
        elif src_piece.name == 'PAWN':
            if src_piece.color == 'WHITE':
                src_move_paths = self.chess_path_finder.select_white_pawn_move_positions(src_pos)
            else:
                src_move_paths = self.chess_path_finder.select_black_pawn_move_positions(src_pos)

        for path in src_move_paths:
            print(path.routes)
            if dst_pos in path.routes:
                if path.is_valid_destination(self, dst_pos):
                    return

        raise InvalidPositionError('cannot reach destination({})'.format(dst_pos))

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
                marker = piece.repr_short() if isinstance(piece, ChessPiece) else '.'
                line.append('{}  '.format(marker))
            line.insert(0, '{}  '.format(r))
            lines.append(''.join(line))

        return '\n'.join(lines)
