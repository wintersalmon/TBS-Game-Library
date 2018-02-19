from chess.pieces import ChessPiece


class ChessPieceWhiteQueen(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.QUEEN)


class ChessPieceBlackQueen(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.QUEEN)
