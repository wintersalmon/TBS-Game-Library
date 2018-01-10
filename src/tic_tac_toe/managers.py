from core.error import CustomError
from core.manager import Manager
from core.player import Player
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.game import TicTacToeGame


class TicTacToeManager(Manager):
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


class TicTacToeMutableManager(TicTacToeManager):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def update(self, event):
        try:
            event.update(self.game)
        except Exception as e:
            raise e
        else:
            self.events.append(event)


class TicTacToeCLIWWrapper(TicTacToeMutableManager):
    TILE_MARKERS = ('O', 'X', ' ')

    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def __bool__(self):
        return self.game.status

    def draw(self):
        status_msg = 'RUNNING' if self.game.status else 'STOPPED'
        print('game status: {}'.format(status_msg))

        board_fmt = ''
        for row in self.game.board.tiles:
            for col in row:
                if col == self.game.players[0].name:
                    marker = self.TILE_MARKERS[0]
                elif col == self.game.players[1].name:
                    marker = self.TILE_MARKERS[1]
                else:
                    marker = self.TILE_MARKERS[2]
                board_fmt += '[' + marker + ']'
            board_fmt += '\n'
        print(board_fmt)


class TicTacToeReplayManager(TicTacToeManager):
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
            event = self.events[self._cur_position - 1]
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
