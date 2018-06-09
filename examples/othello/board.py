from tbs.board import Board
from tbs.error import InvalidValueError, InvalidPositionError
from tbs.position import Position


class OthelloBoard(Board):
    MARKER_INIT = 0
    MARKER_BLACK = 1
    MARKER_WHITE = 2
    MARKER_FLIP = 3
    SET_MARKERS = [
        MARKER_BLACK,
        MARKER_WHITE,
    ]

    def __init__(self, tiles=None):
        if tiles is None:
            super().__init__(8, 8, init_value=self.MARKER_INIT)
            self.tiles[3][3] = self.MARKER_BLACK
            self.tiles[3][4] = self.MARKER_WHITE
            self.tiles[4][3] = self.MARKER_WHITE
            self.tiles[4][4] = self.MARKER_BLACK
        else:
            super().__init__(8, 8, init_value=self.MARKER_INIT, tiles=tiles)

        self._flip_tiles = [[None] * self.cols for _ in range(self.rows)]

    @property
    def count(self):
        black, white = 0, 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.tiles[r][c] == self.MARKER_BLACK:
                    black += 1
                elif self.tiles[r][c] == self.MARKER_WHITE:
                    white += 1
        return black, white

    def encode(self):
        return {
            'tiles': self.tiles
        }

    @classmethod
    def decode(cls, **kwargs):
        tiles = kwargs['tiles']
        return cls(tiles=tiles)

    def set(self, row, col, value):
        if value not in self.SET_MARKERS:
            raise InvalidValueError('invalid marker type: {}'.format(value))
        elif self.is_set(row, col):
            raise InvalidPositionError('position already occupied: {}, {}'.format(row, col))
        else:
            flip_positions = self.find_flip_positions(src_row=row, src_col=col, src_marker=value)
            self._flip_tiles[row][col] = flip_positions
            self.flip_all_positions(flip_positions)
            super().set(row, col, value)

    def reset_tile(self, row, col):
        if self._flip_tiles[row][col]:
            self.flip_all_positions(self._flip_tiles[row][col])
            self._flip_tiles[row][col] = None
        super().reset_tile(row, col)

    def flip(self, row, col):
        if self.is_set(row, col):
            self.tiles[row][col] ^= self.MARKER_FLIP
        else:
            raise InvalidPositionError('cannot flip init marker ({}, {}: {})'.format(row, col, self.tiles[row][col]))

    def is_outer_edge(self, row, col):
        positions = (
            (row - 1, col),  # top
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1),  # right

            (row - 1, col - 1),  # top left
            (row - 1, col + 1),  # top right
            (row + 1, col - 1),  # down left
            (row + 1, col + 1),  # down right
        )

        valid_positions = [(row, col) for row, col in positions if 0 <= row < 8 and 0 <= col < 8]

        for row, col in valid_positions:
            if self.is_set(row, col):
                return True
        return False

    def flip_all_positions(self, positions):
        for pos in positions:
            self.flip(row=pos.row, col=pos.col)

    def find_flip_positions(self, src_row, src_col, src_marker):
        """returns empty list if position is already occupied or not outer edge"""
        if self.is_set(src_row, src_col) or not self.is_outer_edge(src_row, src_col):
            return list()
        else:
            positions = self._collect_line_positions(src_row, src_col, src_marker)
            return [Position(r, c) for r, c in positions]

    def _collect_line_positions(self, row, col, marker):
        positions = list()

        positions += self._line_tracker(row, col, marker, -1, 0)  # up
        positions += self._line_tracker(row, col, marker, 1, 0)  # down
        positions += self._line_tracker(row, col, marker, 0, -1)  # left
        positions += self._line_tracker(row, col, marker, 0, 1)  # right

        positions += self._line_tracker(row, col, marker, -1, -1)  # up left
        positions += self._line_tracker(row, col, marker, -1, 1)  # up right
        positions += self._line_tracker(row, col, marker, 1, -1)  # down left
        positions += self._line_tracker(row, col, marker, 1, 1)  # down right

        return positions

    def _line_tracker(self, row, col, marker, r_off, c_off):
        def move(r, c):
            return r + r_off, c + c_off

        if r_off == 0 and c_off == 0:
            return list()

        positions = list()
        try:
            while True:
                row, col = move(row, col)
                if row < 0 or col < 0:
                    raise IndexError
                elif self.tiles[row][col] == self.MARKER_INIT:
                    raise IndexError
                elif self.tiles[row][col] == marker:
                    break
                else:
                    positions.append((row, col))

        except IndexError:
            positions = list()

        return positions
