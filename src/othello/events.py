from collections import Sequence

from core.error import InvalidPositionError
from core.event import Event
from core.position import Position


class PlayerPlacementEvent(Event):
    def __init__(self, row: int, col: int, marker: int, flip_positions: Sequence):
        self._row = row
        self._col = col
        self._marker = marker
        self._flip_positions = flip_positions

    def update(self, game):
        game.board.set(self._row, self._col, self._marker)
        game.board.flip_all_positions(self._flip_positions)
        game.status.update(game)

    def rollback(self, game):
        game.board.flip_all_positions(self._flip_positions)
        game.board.reset_tile(self._row, self._col)
        game.status.rollback(game)

    def encode(self):
        return {
            'row': self._row,
            'col': self._col,
            'marker': self._marker,
            'flip_positions': [pos.encode() for pos in self._flip_positions]
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'row': kwargs['row'],
            'col': kwargs['col'],
            'marker': kwargs['marker'],
            'flip_positions': [Position.decode(**pos) for pos in kwargs['flip_positions']]
        }
        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, *, game, **kwargs):
        # verify kwargs
        row = cls.get_argument_or_raise_error(kwargs, 'row')
        col = cls.get_argument_or_raise_error(kwargs, 'col')

        player_marker = game.status.turn_player
        flip_positions = game.board.find_flip_positions(row, col, player_marker)

        if len(flip_positions) == 0:
            raise InvalidPositionError(
                'invalid position ({}, {}), has not target to flip'.format(row, col, player_marker))
        else:
            return PlayerPlacementEvent(row=row, col=col, marker=player_marker, flip_positions=flip_positions)
