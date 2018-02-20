from core.utils import SerializableMixin


class Event(SerializableMixin):
    def update(self, game):
        raise NotImplementedError

    def rollback(self, game):
        raise NotImplementedError

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, *, game, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_argument_or_raise_error(cls, kwargs, key):
        try:
            value = kwargs[key]
        except KeyError:
            raise AttributeError('missing attribute ' + key)
        else:
            return value

    def __str__(self):
        return '{}{}'.format(self.__class__.__name__, tuple(self.__dict__.values()))
