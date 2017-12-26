class Board(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = [[None] * cols for _ in range(rows)]

    def __repr__(self):
        lines = list()
        for row in self.tiles:
            lines.append(str(row))
        return '\n'.join(lines)
