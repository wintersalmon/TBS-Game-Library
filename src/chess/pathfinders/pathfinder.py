from chess.pathfinders.base import BasePathFinder
from core.position import Position


class ChessPathFinder(BasePathFinder):
    VALID_DST_EMPTY = 0b1
    VALID_DST_DIFF = 0b10
    VALID_DST_EMPTY_OR_DIFF = 0b11

    def __init__(self):
        super().__init__(min_row=0, max_row=8, min_col=0, max_col=8)

    @classmethod
    def convert_tuple_into_position(cls, positions):
        return [Position(r, c) for r, c in positions]

    def _create_paths_variables(self, src_position):
        raise NotImplementedError

    def search_valid_positions(self, board, src):
        path_variables = self._create_paths_variables(src)

        for variables in path_variables:
            variables['routes'] = self._select_inbound_positions(variables['routes'])

        valid_positions = list()
        for variables in path_variables:
            positions = self.create_valid_destinations(board=board, **variables)
            valid_positions += positions
        return self.convert_tuple_into_position(valid_positions)

    @classmethod
    def create_valid_destinations(cls, board, source, routes, valid_dst=None):
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


class ChessKingPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        count = 1

        return (
            {
                'source': src_position,
                'routes': (self.move_up(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_right(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_up_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_up_right(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down_right(*src_position, count)),
            },
        )


class ChessQueenPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        count = 8

        return (
            {
                'source': src_position,
                'routes': (self.move_up(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_right(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_up_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_up_right(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down_right(*src_position, count)),
            },
        )


class ChessRookPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        count = 8

        return (
            {
                'source': src_position,
                'routes': (self.move_up(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_right(*src_position, count)),
            },
        )


class ChessBishopPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        count = 8

        return (
            {
                'source': src_position,
                'routes': (self.move_up_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_up_right(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down_left(*src_position, count)),
            },
            {
                'source': src_position,
                'routes': (self.move_down_right(*src_position, count)),
            },
        )


class ChessKnightPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        row, col = src_position

        return (
            {
                'source': src_position,
                'routes': ((row - 2, col - 1),)
            },
            {
                'source': src_position,
                'routes': ((row - 2, col + 1),),
            },
            {
                'source': src_position,
                'routes': ((row + 2, col - 1),),
            },
            {
                'source': src_position,
                'routes': ((row + 2, col + 1),),
            },

            {
                'source': src_position,
                'routes': ((row - 1, col - 2),),
            },
            {
                'source': src_position,
                'routes': ((row + 1, col - 2),),
            },
            {
                'source': src_position,
                'routes': ((row - 1, col + 2),),
            },
            {
                'source': src_position,
                'routes': ((row + 1, col + 2),),
            },
        )


class ChessBlackPawnPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        if src_position.row == 6:
            forward_count = 2
        else:
            forward_count = 1

        return (
            {
                'source': src_position,
                'routes': (self.move_up(*src_position, forward_count)),
                'valid_dst': self.VALID_DST_EMPTY
            },
            {
                'source': src_position,
                'routes': (self.move_up_left(*src_position, 1)),
                'valid_dst': self.VALID_DST_DIFF
            },
            {
                'source': src_position,
                'routes': (self.move_up_right(*src_position, 1)),
                'valid_dst': self.VALID_DST_DIFF
            },
        )


class ChessWhitePawnPathFinder(ChessPathFinder):
    def _create_paths_variables(self, src_position):
        if src_position.row == 1:
            forward_count = 2
        else:
            forward_count = 1

        return (
            {
                'source': src_position,
                'routes': (self.move_down(*src_position, forward_count)),
                'valid_dst': self.VALID_DST_EMPTY
            },
            {
                'source': src_position,
                'routes': (self.move_down_left(*src_position, 1)),
                'valid_dst': self.VALID_DST_DIFF
            },
            {
                'source': src_position,
                'routes': (self.move_down_right(*src_position, 1)),
                'valid_dst': self.VALID_DST_DIFF
            },
        )
