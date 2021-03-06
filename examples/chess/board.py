from chess.piece import ChessPiece
from tbs.board import Board
from tbs.error import InvalidValueError


class ChessBoard(Board):
    def __init__(self, tiles=None):
        if tiles is None:
            super().__init__(8, 8, init_value=' ')
            self._init_chess_pieces()
        else:
            super().__init__(8, 8, init_value=' ', tiles=tiles)

    def _init_chess_pieces(self):
        encoded_tiles = [
            'RNBQKBNR',
            'PPPPPPPP',
            '        ',
            '        ',
            '        ',
            '        ',
            'pppppppp',
            'rnbqkbnr',
        ]

        for r, rows in enumerate(encoded_tiles):
            for c, col in enumerate(rows):
                try:
                    tile = ChessPiece.decode(col)
                except InvalidValueError:
                    tile = ' '
                self.tiles[r][c] = tile

    def _get_encode_tiles(self):
        # Because of: ChessPiece.encode() == str(ChessPiece)
        return [[str(col) for col in row] for row in self.tiles]

    def encode(self):
        encoded_tiles = self._get_encode_tiles()
        encoded_tiles = [''.join(row) for row in encoded_tiles]
        return {'tiles': encoded_tiles}

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
