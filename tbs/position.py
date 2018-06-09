from tbs.utils import ImmutableMixin


class Position(ImmutableMixin):
    __slots__ = ('row', 'col')

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __getitem__(self, item):
        return (self.row, self.col)[item]

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

    def __position_compare(self, other):
        if isinstance(other, Position):
            return self.row - other.row, self.col - other.col
        raise NotImplementedError

    def __position_equals(self, other):
        return self.__position_compare(other) == (0, 0)

    def __eq__(self, other):
        if isinstance(other, Position):
            return (self.row, self.col) == (other.row, other.col)
        raise NotImplementedError

    def __ne__(self, other):
        if isinstance(other, Position):
            return (self.row, self.col) != (other.row, other.col)
        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, Position):
            return (self.row, self.col) > (other.row, other.col)
        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, Position):
            return (self.row, self.col) >= (other.row, other.col)
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, Position):
            return (self.row, self.col) < (other.row, other.col)
        raise NotImplementedError

    def __le__(self, other):
        if isinstance(other, Position):
            return (self.row, self.col) <= (other.row, other.col)
        raise NotImplementedError

    def __hash__(self):
        return hash((self.row, self.col))
