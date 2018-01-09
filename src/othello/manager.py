from core.manager import Manager
from othello.events import PlayerPlacementEvent
from othello.game import OthelloGame


class OthelloManager(Manager):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def update(self, event):
        try:
            event.update(self.game)
        except Exception as e:
            raise e
        else:
            self.events.append(event)

    def encode(self):
        return {
            'init_data': self.settings,
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'init_data': kwargs['init_data'],
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }
        return cls.create(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        init_data = kwargs['init_data']
        events = kwargs['events'] if 'events' in kwargs else None
        game = OthelloGame(**init_data)

        manager = OthelloManager(settings=init_data, game=game, events=list())

        if events is not None:
            for event in events:
                manager.update(event)

        return manager
