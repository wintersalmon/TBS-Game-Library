from chess.pieces import ChessPiece


class ChessPieceWhiteRook(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.ROOK)


class ChessPieceBlackRook(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.ROOK)
