from core.board import Board
from core.error import InvalidValueError, InvalidPositionError
from core.position import Position


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

    @property
    def count(self):
        count = -4
        for r in range(self.rows):
            for c in range(self.cols):
                if self.is_set(r, c):
                    count += 1
        return count

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
            super().set(row, col, value)

    def flip(self, row, col):
        if self.is_set(row, col):
            self.tiles[row][col] ^= self.MARKER_FLIP
        else:
            raise InvalidPositionError('cannot flip init marker ({}, {}: {})'.format(row, col, self.tiles[row][col]))

    def has_adjacent_tile(self, row, col):
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
        # if src position is already set or does not have adjacent tile return empty list
        if self.is_set(src_row, src_col) or not self.has_adjacent_tile(src_row, src_col):
            return list()

        flip_targets = set()

        candidate_collections = self._find_flip_candidates(src_row, src_col)
        for candidates in candidate_collections.values():
            flip_targets.update(self._find_flip_targets(src_row, src_col, src_marker, candidates))

        return [Position(r, c) for r, c in flip_targets]

    def _find_flip_candidates(self, src_row, src_col):
        # find horizontal tiles
        horizontal_flip_candidates = set()
        for c in range(self.cols):
            horizontal_flip_candidates.add((src_row, c))

        # find vertical tiles
        vertical_flip_candidates = set()
        for r in range(self.rows):
            vertical_flip_candidates.add((r, src_col))

        # find diagonal left-top to right-bottom tiles
        pos1 = set(zip(reversed(range(src_row)), reversed(range(src_col))))
        pos2 = set(zip(range(src_row, self.rows), range(src_col, self.cols)))
        pos_diagonal = {(src_row, src_col)} | pos1 | pos2
        diagonal_lt_to_rb_flip_candidates = {(r, c) for r, c in pos_diagonal if
                                             (0 <= r < self.rows) and (0 <= c < self.cols)}

        # find diagonal left-bottom to right-top tiles
        pos1 = set(zip(range(src_row, -1, -1), range(src_col, 8)))
        pos2 = set(zip(reversed(range(self.rows, src_row, -1)), reversed(range(0, src_col))))
        pos_diagonal = {(src_row, src_col)} | pos1 | pos2
        diagonal_lb_to_rt_flip_candidates = {(r, c) for r, c in pos_diagonal if
                                             (0 <= r < self.rows) and (0 <= c < self.cols)}

        flip_candidate_collections = {
            'horizontal': horizontal_flip_candidates,
            'vertical': vertical_flip_candidates,
            'diagonal_lt_to_rb ': diagonal_lt_to_rb_flip_candidates,
            'diagonal_lb_to_rt ': diagonal_lb_to_rt_flip_candidates
        }

        return flip_candidate_collections

    def _find_flip_targets(self, src_row, src_col, src_marker, candidates):
        src_pos = (src_row, src_col)
        sorted_candidates = sorted(candidates)
        pos_left_end_idx = 0
        pos_right_start_idx = 0

        for idx, pos in enumerate(sorted_candidates):
            if pos >= src_pos:
                pos_left_end_idx = idx
                break

        for idx, pos in enumerate(sorted_candidates[pos_left_end_idx:], pos_left_end_idx):
            if pos > src_pos:
                pos_right_start_idx = idx
                break

        left_positions = sorted_candidates[:pos_left_end_idx]
        right_positions = sorted_candidates[pos_right_start_idx:]
        target_positions = set()

        for positions in (reversed(left_positions), right_positions):
            can_mark_tiles = False
            marked_positions = set()
            for r, c in positions:
                dst_tile = self.tiles[r][c]
                if dst_tile == self.MARKER_INIT:
                    can_mark_tiles = False
                    break
                elif dst_tile == src_marker:
                    can_mark_tiles = True
                    break
                marked_positions.add((r, c))

            if can_mark_tiles:
                target_positions.update(marked_positions)

        return target_positions
