from core.utils import Serializable


class Wrapper(Serializable):
    def __init__(self, settings, game, events):
        self.settings = settings
        self.game = game
        self.events = events

    def view(self):
        raise NotImplementedError

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError
