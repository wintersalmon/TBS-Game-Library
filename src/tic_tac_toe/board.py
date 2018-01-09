from core.board import Board


class TTTBoard(Board):
    def __init__(self, *, tiles=None):
        super().__init__(rows=3, cols=3, init_value=None, tiles=tiles)

    def encode(self):
        return {
            'tiles': self.tiles
        }

    @classmethod
    def decode(cls, **kwargs):
        tiles = kwargs['tiles']
        return cls(tiles=tiles)

    def __repr__(self):
        lines = list()
        for row in self.tiles:
            lines.append(str(row))
        return '\n'.join(lines)

    def has_bingo(self):
        # horizontal
        for row in self.tiles:
            if (None not in row) and len(set(row)) == 1:
                return True

        # vertical
        for col_idx in range(self.cols):
            patterns = set()
            for row_idx in range(self.rows):
                patterns.add(self.tiles[row_idx][col_idx])

            if (None not in patterns) and len(patterns) == 1:
                return True

        # diagonal left-top right-bottom
        patterns = set()
        for row_idx in range(self.rows):
            for col_idx in range(self.cols):
                if row_idx == col_idx:
                    patterns.add(self.tiles[row_idx][col_idx])

        if (None not in patterns) and len(patterns) == 1:
            return True

        # diagonal left-bottom right-top
        patterns = set()
        for row_idx in range(self.rows):
            for col_idx in range(self.cols):
                if (row_idx + col_idx) == 2:
                    patterns.add(self.tiles[row_idx][col_idx])

        if (None not in patterns) and len(patterns) == 1:
            return True

        return False
