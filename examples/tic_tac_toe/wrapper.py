from tbs.player import Player
from tbs.wrapper import Wrapper
from tic_tac_toe.data.events import PlayerPlacementEvent
from tic_tac_toe.data.game import TicTacToeGame


class TicTacToeWrapper(Wrapper):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'settings': kwargs['settings'],
            'game': cls.create_game_from_settings(**kwargs['settings']),
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create_game_from_settings(cls, **kwargs):
        players = [Player(p) for p in kwargs['player_names']]
        game = TicTacToeGame(players=players)
        return game

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        game = cls.create_game_from_settings(**settings)
        events = list()
        return cls(settings=settings, game=game, events=events)
