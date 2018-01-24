from chess.paths.path import ChessPiecePath
from core.position import Position


class BasePathFinder(object):
    @classmethod
    def get_fixed_values(cls, start, count):
        return (start for _ in range(count))

    @classmethod
    def get_increased_values(cls, start, count):
        start += 1
        return map(lambda offset: start + offset, range(count))

    @classmethod
    def get_decreased_values(cls, start, count):
        start -= 1
        return map(lambda offset: start - offset, range(count))

    @classmethod
    def move_up(cls, row, col, count):
        rows = cls.get_decreased_values(row, count)
        cols = cls.get_fixed_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_down(cls, row, col, count):
        rows = cls.get_increased_values(row, count)
        cols = cls.get_fixed_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_left(cls, row, col, count):
        rows = cls.get_fixed_values(row, count)
        cols = cls.get_decreased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_right(cls, row, col, count):
        rows = cls.get_fixed_values(row, count)
        cols = cls.get_increased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_up_left(cls, row, col, count):
        rows = cls.get_decreased_values(row, count)
        cols = cls.get_decreased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_up_right(cls, row, col, count):
        rows = cls.get_decreased_values(row, count)
        cols = cls.get_increased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_down_left(cls, row, col, count):
        rows = cls.get_increased_values(row, count)
        cols = cls.get_decreased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_down_right(cls, row, col, count):
        rows = cls.get_increased_values(row, count)
        cols = cls.get_increased_values(col, count)

        return list(zip(rows, cols))


class ChessPathFinder(BasePathFinder):
    def __init__(self):
        self.min_row = 0
        self.max_row = 8
        self.min_col = 0
        self.max_col = 8

    def _select_valid_positions(self, positions):
        idx = 0
        for row, col in positions:
            if row < self.min_row:
                return positions[:idx]
            elif row >= self.max_row:
                return positions[:idx]
            elif col < self.min_col:
                return positions[:idx]
            elif col >= self.max_col:
                return positions[:idx]
            else:
                idx += 1
        return positions

    @classmethod
    def convert_tuple_into_position(cls, positions):
        return [Position(r, c) for r, c in positions]

    def select_king_move_positions(self, src_position):
        directions = (
            (self.move_up, 1),
            (self.move_down, 1),
            (self.move_left, 1),
            (self.move_right, 1),
        )

        paths = list()
        for direction, count in directions:
            positions = direction(src_position.row, src_position.col, count)
            valid_positions = self._select_valid_positions(positions)
            if valid_positions:
                valid_routes = self.convert_tuple_into_position(valid_positions)
                paths.append(ChessPiecePath(source=src_position, routes=valid_routes))

        return paths

    def select_queen_move_positions(self, src_position):
        directions = (
            (self.move_up, 8),
            (self.move_down, 8),
            (self.move_left, 8),
            (self.move_right, 8),

            (self.move_up_left, 8),
            (self.move_up_right, 8),
            (self.move_down_left, 8),
            (self.move_down_right, 8),
        )

        paths = list()
        for direction, count in directions:
            positions = direction(src_position.row, src_position.col, count)
            valid_positions = self._select_valid_positions(positions)
            if valid_positions:
                valid_routes = self.convert_tuple_into_position(valid_positions)
                paths.append(ChessPiecePath(source=src_position, routes=valid_routes))

        return paths

    def select_rook_move_positions(self, src_position):
        directions = (
            (self.move_up, 8),
            (self.move_down, 8),
            (self.move_left, 8),
            (self.move_right, 8),
        )

        paths = list()
        for direction, count in directions:
            positions = direction(src_position.row, src_position.col, count)
            valid_positions = self._select_valid_positions(positions)
            if valid_positions:
                valid_routes = self.convert_tuple_into_position(valid_positions)
                paths.append(ChessPiecePath(source=src_position, routes=valid_routes))

        return paths

    def select_bishop_move_positions(self, src_position):
        directions = (
            (self.move_up_left, 8),
            (self.move_up_right, 8),
            (self.move_down_left, 8),
            (self.move_down_right, 8),
        )

        paths = list()
        for direction, count in directions:
            positions = direction(src_position.row, src_position.col, count)
            valid_positions = self._select_valid_positions(positions)
            if valid_positions:
                valid_routes = self.convert_tuple_into_position(valid_positions)
                paths.append(ChessPiecePath(source=src_position, routes=valid_routes))

        return paths

    def select_knight_move_positions(self, src_position):
        src_row = src_position.row
        src_col = src_position.col
        all_positions = [
            [(src_row - 2, src_col - 1)],
            [(src_row - 2, src_col + 1)],
            [(src_row + 2, src_col - 1)],
            [(src_row + 2, src_col + 1)],
            [(src_row - 1, src_col + 2)],
            [(src_row + 1, src_col + 2)],
            [(src_row - 1, src_col - 2)],
            [(src_row + 1, src_col - 2)],
        ]

        paths = list()
        for positions in all_positions:
            valid_positions = self._select_valid_positions(positions)
            if valid_positions:
                valid_routes = self.convert_tuple_into_position(valid_positions)
                paths.append(ChessPiecePath(source=src_position, routes=valid_routes, skip_obstacles=True))

        return paths

    def select_black_pawn_move_positions(self, src_position):
        if src_position.row == 6:
            forward_count = 2
        else:
            forward_count = 1

        forward_positions = self.move_up(src_position.row, src_position.col, forward_count)
        left_positions = self.move_up_left(src_position.row, src_position.col, 1)
        right_positions = self.move_up_right(src_position.row, src_position.col, 1)

        valid_forward_positions = self._select_valid_positions(forward_positions)
        valid_left_positions = self._select_valid_positions(left_positions)
        valid_right_positions = self._select_valid_positions(right_positions)

        valid_forward_routes = self.convert_tuple_into_position(valid_forward_positions)
        valid_left_routes = self.convert_tuple_into_position(valid_left_positions)
        valid_right_routes = self.convert_tuple_into_position(valid_right_positions)

        paths = list()
        if valid_forward_routes:
            valid_forward_path = ChessPiecePath(source=src_position,
                                                routes=valid_forward_routes,
                                                valid_dst=ChessPiecePath.VALID_DST_EMPTY)
            paths.append(valid_forward_path)

        if valid_left_routes:
            valid_left_path = ChessPiecePath(source=src_position,
                                             routes=valid_left_routes,
                                             valid_dst=ChessPiecePath.VALID_DST_DIFF)
            paths.append(valid_left_path)

        if valid_right_routes:
            valid_right_path = ChessPiecePath(source=src_position,
                                              routes=valid_right_routes,
                                              valid_dst=ChessPiecePath.VALID_DST_DIFF)
            paths.append(valid_right_path)

        return paths

    def select_white_pawn_move_positions(self, src_position):
        if src_position.row == 1:
            forward_count = 2
        else:
            forward_count = 1

        forward_positions = self.move_down(src_position.row, src_position.col, forward_count)
        left_positions = self.move_down_left(src_position.row, src_position.col, 1)
        right_positions = self.move_down_right(src_position.row, src_position.col, 1)

        valid_forward_positions = self._select_valid_positions(forward_positions)
        valid_left_positions = self._select_valid_positions(left_positions)
        valid_right_positions = self._select_valid_positions(right_positions)

        valid_forward_routes = self.convert_tuple_into_position(valid_forward_positions)
        valid_left_routes = self.convert_tuple_into_position(valid_left_positions)
        valid_right_routes = self.convert_tuple_into_position(valid_right_positions)

        paths = list()
        if valid_forward_routes:
            valid_forward_path = ChessPiecePath(source=src_position,
                                                routes=valid_forward_routes,
                                                valid_dst=ChessPiecePath.VALID_DST_EMPTY)
            paths.append(valid_forward_path)

        if valid_left_routes:
            valid_left_path = ChessPiecePath(source=src_position,
                                             routes=valid_left_routes,
                                             valid_dst=ChessPiecePath.VALID_DST_DIFF)
            paths.append(valid_left_path)

        if valid_right_routes:
            valid_right_path = ChessPiecePath(source=src_position,
                                              routes=valid_right_routes,
                                              valid_dst=ChessPiecePath.VALID_DST_DIFF)
            paths.append(valid_right_path)

        return paths
