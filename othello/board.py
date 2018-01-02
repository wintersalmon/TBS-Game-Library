class Tile(object):
    BLACK = -1
    INIT = 0
    WHITE = 1

    def __init__(self):
        self._value = self.INIT

    def __bool__(self):
        return self._value is not self.INIT


class Board(object):
    MARKER_BLACK = -1
    MARKER_INIT = 0
    MARKER_WHITE = 1
    MARKER_FLIP = -1

    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.tiles = [[self.MARKER_INIT] * self.cols for _ in range(self.rows)]
        self.markers = [
            self.MARKER_BLACK,
            self.MARKER_WHITE
        ]
        self.last_used_marker = 0
        self.tiles[3][3] = self.MARKER_BLACK
        self.tiles[3][4] = self.MARKER_WHITE
        self.tiles[4][3] = self.MARKER_WHITE
        self.tiles[4][4] = self.MARKER_BLACK

    def has(self, row, col):
        return self.tiles[row][col] is not self.MARKER_INIT

    def get(self, row, col):
        return self.tiles[row][col]

    def set(self, row, col):
        try:
            if self.has(row, col):
                raise ValueError('marker already exist')
            prev_marker = self.tiles[row][col]
        except IndexError:
            raise ValueError('invalid position: {}, {}'.format(row, col))

        try:
            self.tiles[row][col] = self.markers[self.last_used_marker]
            self._find_and_flip_all(row, col)
        except Exception as e:
            self.tiles[row][col] = prev_marker
            raise e
        else:
            self.last_used_marker = (self.last_used_marker + 1) % 2

    def _find_and_flip_all(self, row, col):
        # find horizontal tiles
        pos_horizontal = set()
        for c in range(8):
            pos_horizontal.add((row, c))

        # find vertical tiles
        pos_vertical = set()
        for r in range(8):
            pos_vertical.add((r, col))

        # find diagonal left-top to right-bottom tiles
        pos1 = set(zip(reversed(range(row)), reversed(range(col))))
        pos2 = set(zip(range(row, 8), range(col, 8)))
        pos_diagonal = {(row, col)} | pos1 | pos2
        pos_diagonal_lt_to_rb = {(r, c) for r, c in pos_diagonal if (0 <= r < 8) and (0 <= c < 8)}

        # find diagonal left-bottom to right-top tiles
        pos1 = set(zip(range(row, -1, -1), range(col, 8)))
        pos2 = set(zip(reversed(range(8, row, -1)), reversed(range(0, col))))
        pos_diagonal = {(row, col)} | pos1 | pos2
        pos_diagonal_lb_to_rt = {(r, c) for r, c in pos_diagonal if (0 <= r < 8) and (0 <= c < 8)}

        # check and mark correct position
        all_target_positions = set()
        all_positions = (pos_horizontal, pos_vertical, pos_diagonal_lt_to_rb, pos_diagonal_lb_to_rt)
        for positions in all_positions:
            targets = self._find_flip_target_positions(positions, row, col)
            all_target_positions.update(targets)

        if all_target_positions:
            self._flip_all(all_target_positions)
        else:
            raise ValueError('invalid position')

    def _find_target_positions(self, row, col):
        pass

    def _find_flip_target_positions(self, positions, src_row, src_col):
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

        src_tile = self.tiles[src_row][src_col]
        for positions in (reversed(left_positions), right_positions):

            can_mark_tiles = False
            marked_positions = set()
            for r, c in positions:
                dst_tile = self.tiles[r][c]
                if dst_tile == self.MARKER_INIT:
                    can_mark_tiles = False
                    break
                elif dst_tile == src_tile:
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
        if self.tiles[row][col] is self.MARKER_INIT:
            raise ValueError('cannot flip init marker')
        self.tiles[row][col] *= self.MARKER_FLIP
