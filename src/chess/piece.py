from core.utils import Serializable, ImmutableObject


class ChessPiece(ImmutableObject, Serializable):
    __slots__ = ('name', 'color')

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def encode(self):
        return {
            'name': self.name,
            'color': self.color,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)

    def __repr__(self):
        return '{}:{}'.format(self.name, self.color)
