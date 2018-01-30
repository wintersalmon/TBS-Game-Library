from core.utils import SerializableMixin


class Player(SerializableMixin):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Player({})'.format(self.name)

    def encode(self):
        return {
            'name': self.name
        }

    @classmethod
    def decode(cls, **kwargs):
        name = kwargs['name']
        return cls(name=name)
