from chess.pieces.base import BaseChessPiece
from core.error import InvalidValueError
from core.utils import SerializableMixin, ImmutableMixin


class ChessPiece(BaseChessPiece, ImmutableMixin, SerializableMixin):
    __slots__ = ('_piece', '_color', '_pathfinder')

    def __init__(self, color, piece):
        self._color = self.get_color_value(color)
        self._piece = self.get_piece_value(piece)

        if not self.is_color(self._color):
            raise InvalidValueError('invalid color value ({})'.format(color))

        if not self.is_piece(self._piece):
            raise InvalidValueError('invalid piece value ({})'.format(piece))

        try:
            self._pathfinder = self.PIECE_PATH_FINDERS[self._color][self._piece]
        except KeyError:
            raise InvalidValueError('pathfinder does not exist for values ({}, {})'.format(color, piece))

    @classmethod
    def decode(cls, value):
        return cls(color=value, piece=value)

    def encode(self):
        return self.value

    @property
    def value(self):
        return self._piece | self._color

    @property
    def color(self):
        return self.PIECE_COLORS[self._color]

    @property
    def piece(self):
        return self.PIECE_NAMES[self._piece]

    @property
    def fullname(self):
        return '{}{}'.format(self.color, self.piece)

    @property
    def nickname(self):
        nickname = self.PIECE_NICKNAMES[self._piece]
        if self._color == self.WHITE:
            return nickname.upper()
        else:
            return nickname.lower()

    def search_valid_destinations(self, board, src):
        return self._pathfinder.search_valid_positions(board, src)

    def is_valid_destination(self, board, src, dst):
        return dst in self.search_valid_destinations(board, src)

    def __repr__(self):
        return self.nickname

    def __eq__(self, other):
        if isinstance(other, ChessPiece):
            return (self._color, self._piece) == (other._color, other._piece)
        elif isinstance(other, int):
            return False
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)
