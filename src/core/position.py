from core.utils import ImmutableObject


class Position(ImmutableObject):
    __slots__ = ('row', 'col')

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def encode(self):
        return {
            'row': self.row,
            'col': self.col,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)

    def __repr__(self):
        return '{}({},{})'.format(self.__class__.__name__, self.row, self.col)
