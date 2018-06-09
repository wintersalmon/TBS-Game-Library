from chess.pathfinders.pathfinder import ChessPathFinder


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
