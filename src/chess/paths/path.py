from core.error import InvalidPositionError


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

    def is_valid_destination(self, board, dst_pos):
        if dst_pos not in self.routes:
            raise InvalidPositionError('destination position {} not valid'.format(dst_pos))

        # check obstacles
        if not self.skip_obstacles:
            for pos in self.routes:
                if pos == dst_pos:
                    break
                if board.is_set(pos.row, pos.col):
                    raise InvalidPositionError('dst position({}) should not have obstacles in between'.format(dst_pos))

        # check dst_piece color
        src_piece = board.get(self.source.row, self.source.col)
        dst_piece = board.get(dst_pos.row, dst_pos.col)
        if dst_piece == board.MARKER_INIT:
            return self.valid_dst & self.VALID_DST_EMPTY
        elif dst_piece.color != src_piece.color and self.valid_dst & self.VALID_DST_DIFF:
            return True
        else:
            raise InvalidPositionError('invalid dst pos({}) type'.format(dst_pos))
