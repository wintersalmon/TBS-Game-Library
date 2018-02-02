from chess.pathfinders.base import BasePathFinder
from core.position import Position


class Path(object):
    def __init__(self, source, routes):
        self.source = source
        self.routes = routes

    def __iter__(self):
        for route in self.routes:
            yield route


class ChessPiecePath(Path):
    VALID_DST_EMPTY = 0b1
    VALID_DST_DIFF = 0b10
    VALID_DST_EMPTY_OR_DIFF = 0b11

    def __init__(self, source, routes, *, valid_dst=VALID_DST_EMPTY_OR_DIFF, skip_obstacles=False):
        super().__init__(source=source, routes=routes)
        self.valid_dst = valid_dst
        self.skip_obstacles = skip_obstacles

    # def is_valid_destination(self, board, dst_pos):
    #     return dst_pos in self.get_valid_destinations(board)

    def get_valid_destinations(self, board):
        valid_destinations = list()

        src_piece = board.get(self.source.row, self.source.col)
        for cur_position in self.routes:
            if board.is_set(cur_position.row, cur_position.col):
                dst_piece = board.get(cur_position.row, cur_position.col)
                if src_piece.color != dst_piece.color and self.valid_dst & self.VALID_DST_DIFF:
                    valid_destinations.append(cur_position)

                if self.skip_obstacles:
                    continue
                else:
                    break
            else:
                if self.valid_dst & self.VALID_DST_EMPTY:
                    valid_destinations.append(cur_position)
                    continue
                else:
                    break

        return valid_destinations


class ChessPathFinder(BasePathFinder):
    def __init__(self):
        super().__init__(min_row=0, max_row=8, min_col=0, max_col=8)

    @classmethod
    def convert_tuple_into_position(cls, positions):
        return [Position(r, c) for r, c in positions]

    def find_paths(self, src_position):
        raise NotImplementedError

    def search_valid_positions(self, board, src):
        possible_paths = self.find_paths(src)
        valid_positions = list()
        for path in possible_paths:
            positions = path.get_valid_destinations(board)
            valid_positions += positions
        return valid_positions


class ChessKingPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
        directions = (
            (self.move_up, 1),
            (self.move_down, 1),
            (self.move_left, 1),
            (self.move_right, 1),

            (self.move_up_left, 1),
            (self.move_up_right, 1),
            (self.move_down_left, 1),
            (self.move_down_right, 1),
        )

        paths = list()
        for direction, count in directions:
            positions = direction(src_position.row, src_position.col, count)
            valid_positions = self._select_valid_positions(positions)
            if valid_positions:
                valid_routes = self.convert_tuple_into_position(valid_positions)
                paths.append(ChessPiecePath(source=src_position, routes=valid_routes))

        return paths


class ChessQueenPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
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


class ChessRookPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
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


class ChessBishopPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
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


class ChessKnightPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
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


class ChessBlackPawnPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
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


class ChessWhitePawnPathFinder(ChessPathFinder):
    def find_paths(self, src_position):
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
