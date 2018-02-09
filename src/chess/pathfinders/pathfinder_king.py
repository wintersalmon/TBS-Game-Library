from chess.pathfinders.pathfinder import ChessPieceMoveBehavior


class ChessKingMoveBehavior(ChessPieceMoveBehavior):
    def __init__(self):
        super().__init__(patterns)

    def valid_move_positions(self, board, src):
        positions = set()
        for pattern in self.patterns:
            positions.update(pattern.valid_positions(board, src))
        return list(positions)