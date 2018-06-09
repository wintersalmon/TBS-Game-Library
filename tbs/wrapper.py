from typing import Dict, List

from tbs.event import EventFactory
from tbs.game import Game
from tbs.utils import SerializableMixin


class Wrapper(SerializableMixin):
    cls_game = Game
    event_factory = EventFactory

    def __init__(self, settings: Dict, events: List = None):
        self.settings = settings
        self.game = self.cls_game.create(**self.settings)
        self.events = events if events is not None else list()

    def encode(self):
        return {
            'settings': self.settings,
            'events': [self.event_factory.encode(event) for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_settings = kwargs['settings']
        decoded_events = [cls.event_factory.decode(**e_kwargs) for e_kwargs in kwargs['events']]

        return cls(settings=decoded_settings, events=decoded_events)

    @classmethod
    def create(cls, **kwargs):
        return cls(settings=kwargs)
