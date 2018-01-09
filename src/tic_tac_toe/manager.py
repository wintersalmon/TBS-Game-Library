from core.manager import Manager
from core.player import Player
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.game import TicTacToeGame


class TicTacToeManager(Manager):
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
