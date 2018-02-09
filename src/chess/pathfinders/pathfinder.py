from chess.pathfinders.base import BasePathFinder
from core.position import Position


class ChessPathFinder(BasePathFinder):
    VALID_DST_EMPTY = 0b1
    VALID_DST_DIFF = 0b10
    VALID_DST_EMPTY_OR_DIFF = 0b11

    def __init__(self):
        super().__init__(min_row=0, max_row=8, min_col=0, max_col=8)

    def search_valid_positions(self, board, src):
        path_variables = self._create_paths_variables(src)

        for variables in path_variables:
            variables['routes'] = self._select_inbound_positions(variables['routes'])

        valid_positions = list()
        for variables in path_variables:
            positions = self.select_valid_positions(board=board, **variables)
            valid_positions += positions

        return self.convert_tuple_into_position(valid_positions)

    def _create_paths_variables(self, src_position):
        raise NotImplementedError

    @classmethod
    def convert_tuple_into_position(cls, positions):
        return [Position(r, c) for r, c in positions]

    @classmethod
    def select_valid_positions(cls, board, source, routes, valid_dst=None):
        valid_dst = cls.VALID_DST_EMPTY_OR_DIFF if valid_dst is None else valid_dst
        valid_destinations = list()

        src_piece = board.get(*source)
        for cur_position in routes:
            if board.is_set(*cur_position):
                dst_piece = board.get(*cur_position)
                if src_piece.color != dst_piece.color and valid_dst & cls.VALID_DST_DIFF:
                    valid_destinations.append(cur_position)
            else:
                if valid_dst & cls.VALID_DST_EMPTY:
                    valid_destinations.append(cur_position)
                    continue
                else:
                    break

        return valid_destinations
