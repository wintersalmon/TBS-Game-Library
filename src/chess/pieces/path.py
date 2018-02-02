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
