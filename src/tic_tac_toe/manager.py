from core.manager import Manager
from core.player import Player
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.game import TicTacToeGame


class TicTacToeManager(Manager):
    def __init__(self, init_data, game, events):
        super().__init__(init_data, game, events)

    def update(self, event):
        try:
            event.update(self.game)
        except Exception as e:
            raise e
        else:
            self.events.append(event)

    def encode(self):
        return {
            'init_data': self.init_data,
            'game': self.game.encode(),
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'init_data': kwargs['init_data'],
            'game': TicTacToeGame.decode(**kwargs['game']),
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        init_data = kwargs['init_data']

        data_players = init_data['players']

        players = [Player(p) for p in data_players]

        game = TicTacToeGame(players=players)
        events = kwargs['events'] if 'events' in kwargs else list()

        manager = TicTacToeManager(init_data=init_data, game=game, events=events)

        return manager
