from events.event import Event


class PlayerPlacementEvent(Event):
    def __init__(self, next_marker, row, col):
        self._next_marker = next_marker
        self._row = row
        self._col = col

    def update(self, game):
        prev_marker = game.board.tiles[self._row][self._col]

        if prev_marker is not None:
            raise ValueError('marker already exist')

        game.board.tiles[self._row][self._col] = self._next_marker

    @classmethod
    def create(cls, game, **kwargs):
        # verify kwargs
        name = cls.get_argument_or_raise_error(kwargs, 'name')
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')

        # verify data
        try:
            next_marker = game.players[name].marker
        except KeyError:
            raise ValueError('invalid player name')

        try:
            game.board.tiles[row][col]
        except IndexError:
            raise ValueError('invalid board position row, col')

        # create event and return
        return cls(next_marker=next_marker, row=row, col=col)
