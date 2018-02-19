from chess.pieces import ChessPiece


class ChessPieceWhiteBishop(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.BISHOP)


class ChessPieceBlackBishop(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.BISHOP)
