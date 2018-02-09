from chess.pathfinders.pathfinder import ChessPathFinder


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
