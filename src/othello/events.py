from collections import Sequence

from core.event import Event
from core.position import Position
from othello.errors import PositionHasNoFlipTargetsError


class PlayerPlacementEvent(Event):
    def __init__(self, row, col, marker, flip_positions):
        # verify data type
        if not isinstance(row, int):
            raise ValueError('invalid data type row(int)')

        if not isinstance(col, int):
            raise ValueError('invalid data type col(int)')

        if not isinstance(marker, int):
            raise ValueError('invalid data type marker(int)')

        if not isinstance(flip_positions, Sequence):
            raise ValueError('invalid data type flip_positions(Sequence)')

        self._row = row
        self._col = col
        self._marker = marker
        self._flip_positions = flip_positions

    def update(self, game):
        game.board.set(self._row, self._col, self._marker)
        game.board.flip_all_positions(self._flip_positions)
        game.turn_count += 1

    def rollback(self, game):
        game.board.flip_all_positions(self._flip_positions)
        game.board.reset_tile(self._row, self._col)
        game.turn_count -= 1

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

        player_num = game.get_turn_player_number()
        player_marker = game.board.SET_MARKERS[player_num]
        flip_positions = game.board.find_flip_positions(row, col, player_marker)

        if len(flip_positions) == 0:
            raise PositionHasNoFlipTargetsError(
                'invalid position ({}, {}), has not target to flip'.format(row, col, player_marker))
        else:
            return PlayerPlacementEvent(row=row, col=col, marker=player_marker, flip_positions=flip_positions)
