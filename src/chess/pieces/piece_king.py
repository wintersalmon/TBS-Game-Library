from chess.pieces import ChessPiece


class ChessPieceWhiteKing(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.KING)


class ChessPieceBlackKing(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.KING)
