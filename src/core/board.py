from core.utils import Serializable


class Board(Serializable):
    def __init__(self, rows, cols, *, init_value=None, tiles=None):
        self.rows = rows
        self.cols = cols
        self.init_value = init_value
        if tiles is None:
            tiles = [[init_value] * cols for _ in range(rows)]
        self.tiles = tiles

    def get(self, row, col):
        return self.tiles[row][col]

    def set(self, row, col, value):
        if value is self.init_value:
            raise ValueError('invalid set value {}'.format(value))
        self.tiles[row][col] = value

    def is_set(self, row, col):
        return self.tiles[row][col] is not self.init_value

    def encode(self):
        return {
            'rows': self.rows,
            'cols': self.cols,
            'init_value': self.init_value,
            'tiles': self.tiles
        }

    @classmethod
    def decode(cls, **kwargs):
        rows = kwargs['rows']
        cols = kwargs['cols']
        init_value = kwargs['init_value']
        tiles = kwargs['tiles']

        return cls(rows=rows, cols=cols, init_value=init_value, tiles=tiles)
