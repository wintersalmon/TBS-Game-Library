from chess.piece import ChessPiece
from core.board import Board
from core.error import InvalidValueError


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

    def __repr__(self):
        repr_tiles = [[str(col) for col in row] for row in self.tiles]

        # add row,col number
        for line_num, row in enumerate(repr_tiles):
            row.insert(0, str(line_num))
        repr_tiles.insert(0, [' ', '0', '1', '2', '3', '4', '5', '6', '7'])

        return '\n'.join(['  '.join(row) for row in repr_tiles])
