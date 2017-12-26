from events.event import Event


class PlayerPlacementEvent(Event):
    def __init__(self, row, col, player_name):
        self._row = row
        self._col = col
        self._player_name = player_name

    def update(self, game):
        prev_marker = game.board.tiles[self._row][self._col]

        if prev_marker is not None:
            raise ValueError('marker already exist')

        game.board.tiles[self._row][self._col] = self._player_name

    @classmethod
    def create(cls, game, **kwargs):
        # verify kwargs
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')
        name = cls.get_argument_or_raise_error(kwargs, 'name')

        # verify data
        try:
            game.board.tiles[row][col]
        except IndexError:
            raise ValueError('invalid board position row, col')

        if name in game.players:
            player_name = name
        else:
            raise ValueError('invalid player name')

        # create event and return
        return cls(row=row, col=col, player_name=player_name)
