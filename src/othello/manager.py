from othello.game import OthelloGame
from othello.event import PlayerPlacementEvent


class CallableMixin(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class ManagerFunctionHandler(CallableMixin):
    def __init__(self, manager):
        self.manager = manager

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)

    def function(self, *args, **kwargs):
        raise NotImplementedError


class OthelloDrawHandler(ManagerFunctionHandler):
    def __init__(self, manager):
        super().__init__(manager)

    def function(self):
        markers = [' ', '●', '○']
        for row in range(self.manager.game.board.rows):
            for col in range(self.manager.game.target.board.cols):
                idx = self.manager.game.target.board.tiles[row][col]
                print('[{}]'.format(markers[idx]), end='')
            print()
        print()


class OthelloUpdateHandler(ManagerFunctionHandler):
    def __init__(self, manager):
        super().__init__(manager)

    def function(self, event):
        try:
            self.manager.event.update(self.manager.game)
        except Exception as e:
            raise e
        else:
            self.manager.events.append(event)


class Serializable(object):
    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError


class Manager(Serializable):
    def __init__(self, init_data, game, events, *, draw_handler_class, update_handler_class):
        self.init_data = init_data
        self.game = game
        self.events = events
        self.draw_handler = draw_handler_class(self)
        self.update_handler = update_handler_class(self)

    def encode(self):
        return {
            'init_data': self.init_data,
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'init_data': kwargs['init_data'],
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }
        return cls.create(**decoded_kwargs)

    def update(self, *args, **kwargs):
        self.update_handler(*args, **kwargs)

    def draw(self, *args, **kwargs):
        self.draw_handler(*args, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError


class OthelloManager(Manager):
    def __init__(self, init_data, game, events):
        super().__init__(init_data, game, events,
                         draw_handler_class=OthelloDrawHandler,
                         update_handler_class=OthelloUpdateHandler)

    @classmethod
    def create(cls, **kwargs):
        init_data = kwargs['init_data']
        events = kwargs['events'] if 'events' in kwargs else None
        game = OthelloGame(**init_data)

        manager = OthelloManager(init_data=init_data, game=game, events=list())

        if events is not None:
            for event in events:
                manager.update(event)

        return manager
