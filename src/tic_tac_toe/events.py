from core.error import InvalidPositionError
from core.event import Event


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
        try:
            prev_marker = game.board.tiles[self._row][self._col]
        except IndexError as e:
            raise InvalidPositionError('position out of range: {}, {}'.format(self._row, self._col))

        if prev_marker is not None:
            raise InvalidPositionError('position already occupied: {}'.format(prev_marker))

        game.board.tiles[self._row][self._col] = self._player_name

        game.turn_count += 1
        game.status = not game.board.has_bingo()

    def rollback(self, game):
        game.board.reset_tile(self._row, self._col)

        game.turn_count -= 1
        game.status = not game.board.has_bingo()

    def encode(self):
        return {
            'row': self._row,
            'col': self._col,
            'player_name': self._player_name,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def create(cls, *, game, **kwargs):
        # verify kwargs
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')

        player_name = game.get_turn_player_name()

        return cls(player_name=player_name, row=row, col=col)
