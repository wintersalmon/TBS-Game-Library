from chess.pieces import ChessPiece


class ChessPieceWhitePawn(ChessPiece):
    def __init__(self):
        super().__init__(color=self.WHITE, piece=self.PAWN)


class ChessPieceBlackPawn(ChessPiece):
    def __init__(self):
        super().__init__(color=self.BLACK, piece=self.PAWN)
