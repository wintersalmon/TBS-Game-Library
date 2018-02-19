from chess.pieces import ChessPiece


class ChessPieceWhiteKnight(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.KNIGHT)


class ChessPieceBlackKnight(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.KNIGHT)
