from tbs.utils import SerializableMixin


class Wrapper(SerializableMixin):
    def __init__(self, settings, game, events):
        self.settings = settings
        self.game = game
        self.events = events

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError
