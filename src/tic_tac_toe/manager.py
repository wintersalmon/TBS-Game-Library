from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.game import TicTacToeGame
from tic_tac_toe.handlers import TicTacToeDrawHandler, TicTacToeUpdateHandler
from core.manager import Manager


class TicTacToeManager(Manager):
    def __init__(self, init_data, game, events):
        super().__init__(init_data, game, events,
                         draw_handler_class=TicTacToeDrawHandler,
                         update_handler_class=TicTacToeUpdateHandler)

    def __bool__(self):
        return self.game.status

    def encode(self):
        return {
            'init_data': self.init_data,
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'init_data': kwargs['init_data'],
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }
        return cls.create(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        init_data = kwargs['init_data']
        events = kwargs['events'] if 'events' in kwargs else None
        game = TicTacToeGame(**init_data)

        manager = TicTacToeManager(init_data=init_data, game=game, events=list())
        if events is not None:
            for event in events:
                manager.update(event)

        return manager
