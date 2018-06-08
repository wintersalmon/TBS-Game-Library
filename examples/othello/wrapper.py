from othello.events import PlayerPlacementEvent
from othello.game import OthelloGame
from tbs.player import Player
from tbs.wrapper import Wrapper


class OthelloWrapper(Wrapper):

    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            # 'game': self.game.encode(),
            'events': [event.encode() for event in self.events]
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_settings = kwargs['settings']
        decoded_game = cls.create_game_from_settings(**decoded_settings)
        decoded_events = [PlayerPlacementEvent.decode(**event) for event in kwargs['events']]

        decoded_kwargs = {
            'settings': decoded_settings,
            'game': decoded_game,
            'events': decoded_events
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create_game_from_settings(cls, **kwargs):
        players = [Player(p) for p in kwargs['player_names']]
        return OthelloGame(players=players)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        game = cls.create_game_from_settings(**settings)
        events = list()
        return cls(settings=settings, game=game, events=events)