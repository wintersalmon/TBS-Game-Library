from chess.pathfinders.pathfinder import ChessPathFinder


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
