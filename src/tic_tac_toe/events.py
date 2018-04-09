from core.error import InvalidPositionError
from core.event import Event


class PlayerPlacementEvent(Event):
    def __init__(self, player: int, row: int, col: int):
        self._player = player
        self._row = row
        self._col = col

    def update(self, game):
        if game.board.is_set(self._row, self._col):
            raise InvalidPositionError('position already occupied ({},{})'.format(self._row, self._col))

        game.board.set(self._row, self._col, self._player)
        game.status.update(game)

    def rollback(self, game):
        game.board.reset_tile(self._row, self._col)
        game.status.rollback(game)

    def encode(self):
        return {
            'player': self._player,
            'row': self._row,
            'col': self._col,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def create(cls, *, game, **kwargs):
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')
        player = game.status.turn_player

        return cls(player=player, row=row, col=col)
