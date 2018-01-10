from core.manager import Manager
from core.player import Player
from othello.events import PlayerPlacementEvent
from othello.game import OthelloGame


class OthelloManager(Manager):
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
            'game': OthelloGame.decode(**kwargs['game']),
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        players = [Player(p) for p in kwargs['player_names']]
        game = OthelloGame(players=players)
        events = list()
        return cls(settings=settings, game=game, events=events)


class OthelloViewableManager(OthelloManager):
    VIEW_MARKERS = [' ', '●', '○']

    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def view(self):
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                idx = self.game.board.tiles[row][col]
                print('[{}]'.format(self.VIEW_MARKERS[idx]), end='')
            print()
        print()


class OthelloMutableManager(OthelloViewableManager):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def update(self, event):
        try:
            event.update(self.game)
        except Exception as e:
            raise e
        else:
            self.events.append(event)


class OthelloCLIManager(OthelloMutableManager):
    pass
