class Board(object):
    def __init__(self, rows, cols, *, init_value=None):
        self.rows = rows
        self.cols = cols
        self.init_value = init_value
        self.tiles = [[self.init_value] * cols for _ in range(rows)]

    def get(self, row, col):
        return self.tiles[row][col]

    def set(self, row, col, value):
        self.tiles[row][col] = value

    def is_set(self, row, col):
        if self.tiles[row][col] is not self.init_value:
            return True
        return False
