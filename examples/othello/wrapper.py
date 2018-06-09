from othello.events import PlayerPlacementEvent
from othello.game import OthelloGame
from tbs.wrapper import Wrapper


class OthelloWrapper(Wrapper):

    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            'events': [event.encode() for event in self.events]
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_settings = kwargs['settings']
        decoded_game = OthelloGame.create(**decoded_settings)
        decoded_events = [PlayerPlacementEvent.decode(**event) for event in kwargs['events']]

        return cls(settings=decoded_settings, game=decoded_game, events=decoded_events)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        game = OthelloGame.create(**settings)
        events = list()
        return cls(settings=settings, game=game, events=events)
