class Event(object):
    def update(self, game):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_argument_or_raise_error(cls, kwargs, key):
        try:
            value = kwargs[key]
        except KeyError:
            raise AttributeError('missing attribute ' + key)
        else:
            return value

    def __repr__(self):
        return '{}{}'.format(self.__class__.__name__, tuple(self.__dict__.values()))


class PlayerPlacementEvent(Event):
    def __init__(self, row, col):
        # verify data type
        if not isinstance(row, int):
            raise ValueError('invalid data type row(int)')

        if not isinstance(col, int):
            raise ValueError('invalid data type col(int)')

        self._row = row
        self._col = col

    def update(self, game):
        game.board.set(self._row, self._col)

    @classmethod
    def create(cls, **kwargs):
        # verify kwargs
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')

        return cls(row=row, col=col)
