from core.board import Board

from othello.errors import PositionOutOfBoundsError, PositionAlreadyOccupiedError, PositionHasNoFlipTargetsError, \
    InvalidMarkerTypeError


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

    def encode(self):
        return {
            'tiles': self.tiles
        }

    @classmethod
    def decode(cls, **kwargs):
        tiles = kwargs['tiles']
        return cls(tiles=tiles)

    def set(self, row, col, value):
        # check Marker Type
        if value not in self.SET_MARKERS:
            raise InvalidMarkerTypeError('invalid marker type: {}'.format(value))

        # check PositionOutOfBoundsError
        try:
            prev_marker = self.tiles[row][col]
        except IndexError:
            raise PositionOutOfBoundsError('({}, {})'.format(row, col))

        # check PositionAlreadyOccupiedError
        if prev_marker is not self.MARKER_INIT:
            raise PositionAlreadyOccupiedError('({}, {})'.format(row, col))

        # check PositionHasNoFlipTargetsError
        next_marker = value
        flip_targets = self._find_flip_targets(row, col, next_marker)

        if flip_targets:  # set tile & flip all target tiles
            self.tiles[row][col] = next_marker
            self._flip_all(flip_targets)
        else:
            raise PositionHasNoFlipTargetsError('({}, {})'.format(row, col))

    def _find_flip_targets(self, src_row, src_col, src_marker):
        # find horizontal tiles
        potential_targets_horizontal = set()
        for c in range(8):
            potential_targets_horizontal.add((src_row, c))

        # find vertical tiles
        potential_targets_vertical = set()
        for r in range(8):
            potential_targets_vertical.add((r, src_col))

        # find diagonal left-top to right-bottom tiles
        pos1 = set(zip(reversed(range(src_row)), reversed(range(src_col))))
        pos2 = set(zip(range(src_row, 8), range(src_col, 8)))
        pos_diagonal = {(src_row, src_col)} | pos1 | pos2
        potential_targets_diagonal_lt_to_rb = {(r, c) for r, c in pos_diagonal if (0 <= r < 8) and (0 <= c < 8)}

        # find diagonal left-bottom to right-top tiles
        pos1 = set(zip(range(src_row, -1, -1), range(src_col, 8)))
        pos2 = set(zip(reversed(range(8, src_row, -1)), reversed(range(0, src_col))))
        pos_diagonal = {(src_row, src_col)} | pos1 | pos2
        potential_targets_diagonal_lb_to_rt = {(r, c) for r, c in pos_diagonal if (0 <= r < 8) and (0 <= c < 8)}

        potential_target_collection = (
            potential_targets_horizontal,
            potential_targets_vertical,
            potential_targets_diagonal_lt_to_rb,
            potential_targets_diagonal_lb_to_rt
        )

        # find and save target positions
        targets = set()
        for positions in potential_target_collection:
            cur_targets = self._find_flip_target_positions(positions, src_row, src_col, src_marker)
            targets.update(cur_targets)

        return targets

    def _find_flip_target_positions(self, positions, src_row, src_col, src_marker):
        src_pos = (src_row, src_col)
        sorted_positions = sorted(positions)
        pos_left_end_idx = 0
        pos_right_start_idx = 0

        for idx, pos in enumerate(sorted_positions):
            if pos >= src_pos:
                pos_left_end_idx = idx
                break

        for idx, pos in enumerate(sorted_positions[pos_left_end_idx:], pos_left_end_idx):
            if pos > src_pos:
                pos_right_start_idx = idx
                break

        left_positions = sorted_positions[:pos_left_end_idx]
        right_positions = sorted_positions[pos_right_start_idx:]
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

    def _flip_all(self, positions):
        for r, c in positions:
            self._flip(r, c)

    def _flip(self, row, col):
        if self.is_set(row, col):
            self.tiles[row][col] ^= self.MARKER_FLIP
        else:
            raise ValueError('cannot flip init marker')
