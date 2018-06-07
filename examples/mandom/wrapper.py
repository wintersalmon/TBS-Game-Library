from mandom.data.events import EventCode, EventFactory
from mandom.data.game import MandomGame
from mandom.data.player import Player
from tbs.error import InvalidValueError
from tbs.wrapper import Wrapper


class MandomWrapper(Wrapper):

    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            'events': [self.encode_event(event) for event in self.events]
        }

    @classmethod
    def decode(cls, **kwargs):
        settings = kwargs['settings']
        game = cls.create_game_from_settings(**settings)
        events = [cls.decode_event(code, data) for code, data in kwargs['events']]

        return cls(settings=settings, game=game, events=events)

    @classmethod
    def encode_event(cls, event):
        for event_code, event_cls in EventFactory.EVENTS.items():
            if isinstance(event, event_cls):
                return [event_code.value, event.encode()]
        raise InvalidValueError('invalid event type: {}'.format(event))

    @classmethod
    def decode_event(cls, code, data):
        event_code = EventCode(code)
        event_cls = EventFactory.get(event_code)
        return event_cls.decode(**data)

    @classmethod
    def create_game_from_settings(cls, **settings):
        players = [Player(p) for p in settings['player_names']]
        return MandomGame(players=players)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        game = cls.create_game_from_settings(**settings)
        events = list()
        return cls(settings=settings, game=game, events=events)
