from core.utils import Serializable, ImmutableObject


class ChessPiece(ImmutableObject, Serializable):
    COLOR_BLACK = 'BLACK'
    COLOR_WHITE = 'WHITE'
    KING = 'KING'
    QUEEN = 'QUEEN'
    ROOK = 'ROOK'
    BISHOP = 'BISHOP'
    KNIGHT = 'KNIGHT'
    PAWN = 'PAWN'
    SHORT_NAME = {
        KING: 'K',
        QUEEN: 'Q',
        ROOK: 'R',
        BISHOP: 'B',
        KNIGHT: 'N',
        PAWN: 'P',
    }
    __slots__ = ('name', 'color')

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def encode(self):
        return {
            'name': self.name,
            'color': self.color,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)

    def __repr__(self):
        return '{}:{}'.format(self.name, self.color)

    def repr_short(self):
        short = self.SHORT_NAME[self.name]
        if self.color == self.COLOR_BLACK:
            short = short.lower()
        return short
