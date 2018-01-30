from chess.paths.finder import ChessPathFinder
from chess.piece import ChessPiece, ChessPieceWhitePawn, ChessPieceBlackPawn, ChessPieceWhiteRook, \
    ChessPieceWhiteBishop, ChessPieceWhiteKnight, ChessPieceWhiteQueen, ChessPieceWhiteKing, ChessPieceBlackRook, \
    ChessPieceBlackKnight, ChessPieceBlackBishop, ChessPieceBlackQueen, ChessPieceBlackKing
from core.board import Board
from core.error import InvalidPositionError


class ChessBoard(Board):
    def __init__(self, tiles=None):
        if tiles is None:
            super().__init__(8, 8, init_value=ChessPiece.BLANK)
            self._init_chess_pieces()
        else:
            super().__init__(8, 8, init_value=ChessPiece.BLANK, tiles=tiles)
        self.chess_path_finder = ChessPathFinder()

    def _init_chess_pieces(self):
        self.tiles[0][0] = ChessPieceWhiteRook()
        self.tiles[0][1] = ChessPieceWhiteKnight()
        self.tiles[0][2] = ChessPieceWhiteBishop()
        self.tiles[0][3] = ChessPieceWhiteQueen()
        self.tiles[0][4] = ChessPieceWhiteKing()
        self.tiles[0][5] = ChessPieceWhiteBishop()
        self.tiles[0][6] = ChessPieceWhiteKnight()
        self.tiles[0][7] = ChessPieceWhiteRook()

        self.tiles[1][0] = ChessPieceWhitePawn()
        self.tiles[1][1] = ChessPieceWhitePawn()
        self.tiles[1][2] = ChessPieceWhitePawn()
        self.tiles[1][3] = ChessPieceWhitePawn()
        self.tiles[1][4] = ChessPieceWhitePawn()
        self.tiles[1][5] = ChessPieceWhitePawn()
        self.tiles[1][6] = ChessPieceWhitePawn()
        self.tiles[1][7] = ChessPieceWhitePawn()

        self.tiles[6][0] = ChessPieceBlackPawn()
        self.tiles[6][1] = ChessPieceBlackPawn()
        self.tiles[6][2] = ChessPieceBlackPawn()
        self.tiles[6][3] = ChessPieceBlackPawn()
        self.tiles[6][4] = ChessPieceBlackPawn()
        self.tiles[6][5] = ChessPieceBlackPawn()
        self.tiles[6][6] = ChessPieceBlackPawn()
        self.tiles[6][7] = ChessPieceBlackPawn()

        self.tiles[7][0] = ChessPieceBlackRook()
        self.tiles[7][1] = ChessPieceBlackKnight()
        self.tiles[7][2] = ChessPieceBlackBishop()
        self.tiles[7][3] = ChessPieceBlackQueen()
        self.tiles[7][4] = ChessPieceBlackKing()
        self.tiles[7][5] = ChessPieceBlackBishop()
        self.tiles[7][6] = ChessPieceBlackKnight()
        self.tiles[7][7] = ChessPieceBlackRook()

    def can_move(self, src_pos, dst_pos):
        if not self.is_set(src_pos.row, src_pos.col):
            raise InvalidPositionError('from position({}) should not be empty'.format(src_pos))

        # TODO : clean up required
        src_piece = self.get(src_pos.row, src_pos.col)
        src_move_paths = src_piece.find_paths(src_pos)

        for path in src_move_paths:
            if dst_pos in path.routes:
                if path.is_valid_destination(self, dst_pos):
                    return

        raise InvalidPositionError('cannot reach destination({})'.format(dst_pos))

    def encode(self):
        return {'tiles': self.tiles}

    @classmethod
    def decode(cls, **kwargs):
        tiles = kwargs['tiles']
        return cls(tiles=tiles)

    def __repr__(self):
        # get lines
        header = [' ', '0', '1', '2', '3', '4', '5', '6', '7']
        body = list()
        for row_number, rows in enumerate(self.tiles):
            line = [str(row_number)]
            for col_number, tile in enumerate(rows):
                if self.is_set(row_number, col_number):
                    tile_marker = repr(tile)
                else:
                    tile_marker = '.'
                line.append(tile_marker)
            body.append(line)

        # format lines
        lines = list()
        for line in (header, *body):
            fmt_line = '  '.join(line)
            lines.append(fmt_line)

        return '\n'.join(lines)
