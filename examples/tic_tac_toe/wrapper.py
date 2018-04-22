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
            'game': self.game.encode(),
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'settings': kwargs['settings'],
            'game': TicTacToeGame.decode(**kwargs['game']),
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        players = [Player(p) for p in kwargs['player_names']]
        game = TicTacToeGame(players=players)
        events = list()
        return cls(settings=settings, game=game, events=events)
