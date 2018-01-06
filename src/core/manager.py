class Manager(object):
    def __init__(self, init_data, game, events, *, draw_handler_class, update_handler_class):
        self.init_data = init_data
        self.game = game
        self.events = events
        self.draw_handler = draw_handler_class(self)
        self.update_handler = update_handler_class(self)

    def update(self, *args, **kwargs):
        self.update_handler(*args, **kwargs)

    def draw(self, *args, **kwargs):
        self.draw_handler(*args, **kwargs)

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError
