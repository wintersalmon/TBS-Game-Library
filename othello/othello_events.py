class Event(object):
    def update(self, game):
        raise NotImplementedError

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
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
    def __init__(self, row, col, player):
        # verify data type
        if not isinstance(row, int):
            raise ValueError('invalid data type row(int)')

        if not isinstance(col, int):
            raise ValueError('invalid data type col(int)')

        if not isinstance(player, int):
            raise ValueError('invalid data type player(int)')

        self._row = row
        self._col = col
        self._player = player

    def update(self, game):
        marker = game.board.SET_MARKERS[self._player]
        game.board.set(self._row, self._col, marker)
        game.turn_count += 1

    def encode(self):
        return {
            'row': self._row,
            'col': self._col,
            'player': self._player,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls.create(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        # verify kwargs
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')
        player = cls.get_argument_or_raise_error(kwargs, 'player')

        return cls(row=row, col=col, player=player)
