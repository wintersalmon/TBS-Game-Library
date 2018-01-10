from core.error import CustomError
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


class OthelloReplayManager(OthelloViewableManager):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)
        self._max_position = len(self.events)
        self._cur_position = self._max_position

    def set_position(self, position):
        if 0 <= position <= self._max_position:
            pos_difference = position - self._cur_position
            pos_offset = abs(pos_difference)

            if pos_difference >= 0:
                move_to_direction = self.forward
            else:
                move_to_direction = self.backward

            while pos_offset > 0:
                move_to_direction()
                pos_offset -= 1

    def get_max_position(self):
        return self._max_position

    def get_position(self):
        return self._cur_position

    def forward(self):
        if self._cur_position < self._max_position:
            event = self.events[self._cur_position]
            event.update(self.game)
            self._cur_position += 1
            return True
        raise CustomError('Impossible to move forward')

    def backward(self):
        if self._cur_position >= 0:
            event = self.events[self._cur_position - 1]
            event.rollback(self.game)
            self._cur_position -= 1
            return True
        raise CustomError('Impossible to move backward')

    def __repr__(self):
        return '{}/{}'.format(self._cur_position, self._max_position)
