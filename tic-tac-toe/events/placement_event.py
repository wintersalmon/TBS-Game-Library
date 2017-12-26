from events.event import Event


class PlayerPlacementEvent(Event):
    def __init__(self, player_name, row, col):
        # verify data type
        if not isinstance(player_name, str):
            raise ValueError('invalid data type player_name(str)')

        if not isinstance(row, int):
            raise ValueError('invalid data type row(int)')

        if not isinstance(col, int):
            raise ValueError('invalid data type col(int)')

        self._player_name = player_name
        self._row = row
        self._col = col

    def update(self, game):
        prev_marker = game.board.tiles[self._row][self._col]

        if prev_marker is not None:
            raise ValueError('marker already exist')

        game.board.tiles[self._row][self._col] = self._player_name

        game.turn_count += 1
        if game.board.has_bingo():
            game.status = False

    @classmethod
    def create(cls, **kwargs):
        # verify kwargs
        player_name = cls.get_argument_or_raise_error(kwargs, 'player_name')
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')

        return cls(player_name=player_name, row=row, col=col)
