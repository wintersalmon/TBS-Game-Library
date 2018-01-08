class Manager(object):
    def __init__(self, init_data, game, events):
        self.init_data = init_data
        self.game = game
        self.events = events

    def update(self, event):
        raise NotImplementedError

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError
