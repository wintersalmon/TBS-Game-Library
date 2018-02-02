class BasePathFinder(object):
    def __init__(self, min_row, max_row, min_col, max_col):
        self.min_row = min_row
        self.max_row = max_row
        self.min_col = min_col
        self.max_col = max_col

    def _select_valid_positions(self, positions):
        idx = 0
        for row, col in positions:
            if row < self.min_row:
                return positions[:idx]
            elif row >= self.max_row:
                return positions[:idx]
            elif col < self.min_col:
                return positions[:idx]
            elif col >= self.max_col:
                return positions[:idx]
            else:
                idx += 1
        return positions

    @classmethod
    def get_fixed_values(cls, start, count):
        return (start for _ in range(count))

    @classmethod
    def get_increased_values(cls, start, count):
        start += 1
        return map(lambda offset: start + offset, range(count))

    @classmethod
    def get_decreased_values(cls, start, count):
        start -= 1
        return map(lambda offset: start - offset, range(count))

    @classmethod
    def move_up(cls, row, col, count):
        rows = cls.get_decreased_values(row, count)
        cols = cls.get_fixed_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_down(cls, row, col, count):
        rows = cls.get_increased_values(row, count)
        cols = cls.get_fixed_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_left(cls, row, col, count):
        rows = cls.get_fixed_values(row, count)
        cols = cls.get_decreased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_right(cls, row, col, count):
        rows = cls.get_fixed_values(row, count)
        cols = cls.get_increased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_up_left(cls, row, col, count):
        rows = cls.get_decreased_values(row, count)
        cols = cls.get_decreased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_up_right(cls, row, col, count):
        rows = cls.get_decreased_values(row, count)
        cols = cls.get_increased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_down_left(cls, row, col, count):
        rows = cls.get_increased_values(row, count)
        cols = cls.get_decreased_values(col, count)

        return list(zip(rows, cols))

    @classmethod
    def move_down_right(cls, row, col, count):
        rows = cls.get_increased_values(row, count)
        cols = cls.get_increased_values(col, count)

        return list(zip(rows, cols))
