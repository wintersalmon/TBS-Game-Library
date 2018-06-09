from chess.pathfinders.pathfinder import ChessPathFinder


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
