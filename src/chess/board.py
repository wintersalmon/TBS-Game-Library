from chess.pieces import *
from core.board import Board
from core.error import InvalidValueError


class ChessBoard(Board):
    def __init__(self, tiles=None):
        if tiles is None:
            super().__init__(8, 8, init_value=ChessPiece.BLANK)
            self._init_chess_pieces()
        else:
            super().__init__(8, 8, init_value=ChessPiece.BLANK, tiles=tiles)

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

    def encode(self):
        encoded_rows = list()
        for rows in self.tiles:
            encoded_cols = list()
            for col in rows:
                try:
                    encoded_col = col.encode()
                except AttributeError:
                    encoded_col = col
                encoded_cols.append(encoded_col)
            encoded_rows.append(encoded_cols)

        return {'tiles': encoded_rows}

    @classmethod
    def decode(cls, **kwargs):
        decoded_tiles = list()

        for encoded_row in kwargs['tiles']:
            decoded_row = list()
            for encoded_tile in encoded_row:
                try:
                    tile = ChessPiece.decode(encoded_tile)
                except InvalidValueError:
                    tile = encoded_tile
                decoded_row.append(tile)
            decoded_tiles.append(decoded_row)

        return cls(tiles=decoded_tiles)

    # def encode(self):
    #     encoded_tiles = list()
    #
    #     for row in self.tiles:
    #         encoded_row = list()
    #         for tile in row:
    #             try:
    #                 encoded_tile = tile.encode()
    #             except AttributeError:
    #                 encoded_tile = tile
    #             encoded_row.append(encoded_tile)
    #         encoded_tiles.append(encoded_row)
    #
    #     return {'tiles': encoded_tiles}
    #
    # @classmethod
    # def decode(cls, **kwargs):
    #     decoded_tiles = list()
    #
    #     for encoded_row in kwargs['tiles']:
    #         decoded_row = list()
    #         for encoded_tile in encoded_row:
    #             try:
    #                 tile = ChessPiece.decode(**encoded_tile)
    #             except (ValueError, TypeError):
    #                 tile = encoded_tile
    #             decoded_row.append(tile)
    #         decoded_tiles.append(decoded_row)
    #
    #     return cls(tiles=decoded_tiles)

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
