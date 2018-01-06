from othello import Othello
from othello_events import PlayerPlacementEvent


class OthelloManager(object):
    def __init__(self, game, events):
        self._init_data = {
            'player_one': game.player_names[0],
            'player_two': game.player_names[1],
        }
        self.game = game
        self.events = events

    def update(self, event):
        event.update(self.game)
        self.events.append(event)

    @classmethod
    def create(cls, player_one, player_two, *, prev_events=None):
        othello = Othello(player_one, player_two)
        events = list()
        manager = OthelloManager(game=othello, events=events)
        if prev_events is not None:
            for event in prev_events:
                manager.update(event)
        return manager

    def encode(self):
        return {
            'player_one': self._init_data['player_one'],
            'player_two': self._init_data['player_two'],
            'prev_events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'player_one': kwargs['player_one'],
            'player_two': kwargs['player_two'],
            'prev_events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['prev_events']]
        }
        return cls.create(**decoded_kwargs)
