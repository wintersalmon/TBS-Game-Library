from tbs.utils import SerializableMixin


class Game(SerializableMixin):
    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError
