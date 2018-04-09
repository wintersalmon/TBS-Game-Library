from core.player import Player
from core.wrapper import Wrapper
from othello.events import PlayerPlacementEvent
from othello.game import OthelloGame


class OthelloWrapper(Wrapper):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            'game': self.game.encode(),
            'events': [event.encode() for event in self.events]
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_settings = kwargs['settings']
        decoded_game = OthelloGame.decode(**kwargs['game'])
        decoded_events = [PlayerPlacementEvent.decode(**event) for event in kwargs['events']]

        decoded_kwargs = {
            'settings': decoded_settings,
            'game': decoded_game,
            'events': decoded_events
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        players = [Player(p) for p in kwargs['player_names']]
        game = OthelloGame(players=players)
        events = list()
        return cls(settings=settings, game=game, events=events)
